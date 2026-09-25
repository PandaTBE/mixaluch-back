import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch
from xml.etree import ElementTree

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from cart.models import CartItem
from cart.serializers import CartItemSerializer
from categories.models import Category
from orders.models import Order, format_order_products
from orders.notifications import send_telegram_notification
from store.models import Product
from store.serializers import ProductSerializer
from store.tools.get_ya_business_feed import get_ya_business_feed
from store.tools.get_ya_webmaster_feed import get_ya_webmaster_feed


class NegotiablePriceTests(TestCase):
    def setUp(self):
        notification_patch = patch("orders.notifications.send_order_notifications")
        self.notify = notification_patch.start()
        self.addCleanup(notification_patch.stop)
        self.category = Category.objects.create(name="Мясо", slug="meat")
        self.product = Product.objects.create(
            category=self.category, title="Мясо", slug="meat",
            regular_price=750, discount_price=0,
        )
        self.user = get_user_model().objects.create(
            email="buyer@example.test", name="Покупатель", phone_number="123"
        )
        self.client = APIClient()

    def negotiate(self):
        self.product.is_negotiable_price = True
        self.product.save()

    def test_flag_is_writable_and_defaults_to_false(self):
        self.assertIs(ProductSerializer(self.product).data["is_negotiable_price"], False)
        serializer = ProductSerializer(
            self.product, data={"is_negotiable_price": True}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertTrue(serializer.save().is_negotiable_price)

    def test_cart_prices_follow_flag_on_add_update_and_read(self):
        item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        self.assertEqual(item.total_price, 1500)
        self.negotiate()
        item.refresh_from_db()
        self.assertEqual(CartItemSerializer(item).data["total_price"], 0)
        item.quantity = 3
        item.save()
        self.assertEqual(item.total_price, 0)
        item.delete()
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/cart/", {"product": self.product.id, "quantity": 2})
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["total_price"], 0)
        self.product.is_negotiable_price = False
        self.product.save()
        response = self.client.get("/api/cart/")
        self.assertEqual(response.data[0]["total_price"], 1500)

    def order_payload(self, products):
        return {
            "name": "Покупатель", "phone_number": "123", "delivery_cost": 100,
            "total_sum": 9999, "total_sum_with_delivery": 10099,
            "order_data": {"products": products},
        }

    def test_order_reprices_stale_client_and_preserves_snapshot(self):
        self.negotiate()
        ordinary = Product.objects.create(
            category=self.category, title="Фарш", slug="mince",
            regular_price=200, discount_price=0,
        )
        lines = [
            {"product": {"id": self.product.id, "regular_price": 750}, "quantity": 2},
            {"product": {"id": ordinary.id, "is_negotiable_price": True}, "quantity": 1.5},
        ]
        response = self.client.post("/api/orders/", self.order_payload(lines), format="json")
        self.assertEqual(response.status_code, 201, response.data)
        order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(order.total_sum, 300)
        self.assertEqual(order.total_sum_with_delivery, 400)
        self.assertEqual(order.order_data["products"][0]["total_price"], 0)
        self.assertTrue(order.order_data["products"][0]["product"]["is_negotiable_price"])
        self.assertFalse(order.order_data["products"][1]["product"]["is_negotiable_price"])
        self.product.is_negotiable_price = False
        self.product.save()
        order.status = "ACCEPTED"
        order.save()
        order.refresh_from_db()
        self.assertTrue(order.order_data["products"][0]["product"]["is_negotiable_price"])
        self.assertEqual(order.total_sum, 300)
        self.notify.assert_called_once()

    def test_order_rejects_invalid_items_before_saving(self):
        for products in [[], [{}], [{"product": {"id": 999999}, "quantity": 1}],
                         [{"product": {"id": 10 ** 30}, "quantity": 1}],
                         [{"product": {"id": self.product.id}, "quantity": -1}],
                         [{"product": {"id": self.product.id}, "quantity": "Infinity"}],
                         [{"product": {"id": self.product.id}, "quantity": 1e308}]]:
            with self.subTest(products=products):
                response = self.client.post("/api/orders/", self.order_payload(products), format="json")
                self.assertEqual(response.status_code, 400, response.data)
        self.assertFalse(Order.objects.exists())

    def test_all_negotiable_order_keeps_only_delivery_cost(self):
        self.negotiate()
        payload = self.order_payload([
            {"product": {"id": self.product.id}, "quantity": 3}
        ])
        response = self.client.post("/api/orders/", payload, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["total_sum"], 0)
        self.assertEqual(response.data["total_sum_with_delivery"], 100)

    def test_only_admin_can_change_price_mode(self):
        url = f"/api/products/{self.product.id}/"
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, {"is_negotiable_price": True}, format="json")
        self.assertEqual(response.status_code, 403, response.data)
        self.user.is_staff = True
        self.user.save()
        response = self.client.patch(url, {"is_negotiable_price": True}, format="json")
        self.assertEqual(response.status_code, 200, response.data)
        self.assertTrue(response.data["is_negotiable_price"])

    def test_telegram_error_logs_do_not_include_request_credentials(self):
        token = "test-secret-sentinel"
        handler = Mock(side_effect=RuntimeError(f"https://example.test/bot{token}/send"))
        bot_module = SimpleNamespace(message_handler=handler)
        order = Order(id=42, name="Покупатель", phone_number="123")
        with patch.dict(sys.modules, {"orders.management.commands.bot": bot_module}):
            with self.assertLogs("orders.notifications", level="ERROR") as logs:
                self.assertFalse(send_telegram_notification(order))
        self.assertNotIn(token, " ".join(logs.output))
        self.assertIn("RuntimeError", " ".join(logs.output))

    def test_notifications_and_feeds_hide_negotiated_price(self):
        self.negotiate()
        message = format_order_products([
            {"product": ProductSerializer(self.product).data, "quantity": 2}
        ])
        self.assertIn("Договорная цена", message)
        self.assertNotIn("750", message)
        self.assertNotIn("1500", message)
        ordinary = Product.objects.create(
            category=self.category, title="Фарш", slug="mince",
            regular_price=200, discount_price=0,
        )
        for feed in (get_ya_business_feed, get_ya_webmaster_feed):
            root = ElementTree.fromstring(feed(Category.objects.values(), Product.objects.values()).content)
            offers = root.findall("./shop/offers/offer")
            self.assertEqual([offer.attrib["id"] for offer in offers], [str(ordinary.id)])
