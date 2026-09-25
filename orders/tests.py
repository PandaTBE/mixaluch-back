from django.test import TestCase
from rest_framework.test import APIClient

from orders.models import DeliveryType, Order, OrderingSettings


class OrderingSettingsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_anonymous_customer_can_read_delivery_settings(self):
        OrderingSettings.objects.create(
            notice="Самовывоз временно недоступен",
            self_delivery_enabled=False,
            courier_delivery_enabled=True,
        )
        response = self.client.get("/api/ordering-settings/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "notice": "Самовывоз временно недоступен",
            "self_delivery_enabled": False,
            "courier_delivery_enabled": True,
        })

    def test_settings_endpoint_does_not_allow_customer_updates(self):
        settings = OrderingSettings.objects.create(self_delivery_enabled=False)
        response = self.client.patch(
            "/api/ordering-settings/", {"self_delivery_enabled": True}, format="json"
        )
        self.assertEqual(response.status_code, 405)
        settings.refresh_from_db()
        self.assertFalse(settings.self_delivery_enabled)

    def test_disabled_delivery_is_rejected_before_order_creation(self):
        cases = (
            (False, True, DeliveryType.SELF_DELIVERY, "Самовывоз временно недоступен."),
            (True, False, DeliveryType.COURIER_DELIVERY, "Доставка курьером временно недоступна."),
            (False, False, DeliveryType.SELF_DELIVERY, "Оформление заказов временно недоступно."),
            (False, False, DeliveryType.COURIER_DELIVERY, "Оформление заказов временно недоступно."),
        )
        for pickup, courier, delivery_type, message in cases:
            with self.subTest(pickup=pickup, courier=courier, delivery_type=delivery_type):
                OrderingSettings.objects.update_or_create(pk=1, defaults={
                    "self_delivery_enabled": pickup,
                    "courier_delivery_enabled": courier,
                })
                response = self.client.post("/api/orders/", {
                    "name": "Покупатель",
                    "phone_number": "123",
                    "delivery_type": delivery_type,
                    "order_data": {"products": []},
                }, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.data["delivery_type"], [message])
                self.assertFalse(Order.objects.exists())
