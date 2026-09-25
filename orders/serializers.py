import math
from decimal import Decimal

from rest_framework import serializers

from orders.models import DeliveryType, Order, OrderingSettings
from store.models import Product
from store.serializers import ProductSerializer


class OrderProductReferenceSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1, max_value=9223372036854775807)


class OrderingSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderingSettings
        fields = ("notice", "self_delivery_enabled", "courier_delivery_enabled")


class OrderItemInputSerializer(serializers.Serializer):
    product = OrderProductReferenceSerializer()
    quantity = serializers.FloatField()

    def validate_quantity(self, value):
        if not math.isfinite(value) or value <= 0:
            raise serializers.ValidationError("Количество должно быть положительным числом.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {
            "total_sum": {"min_value": 0, "max_value": 2147483647},
            "total_sum_with_delivery": {"min_value": 0, "max_value": 2147483647},
        }

    def validate(self, attrs):
        # Status updates retain the prices agreed when the order was placed.
        if self.instance is not None:
            return attrs
        delivery_type = attrs.get(
            "delivery_type", Order._meta.get_field("delivery_type").get_default()
        )
        settings = OrderingSettings.objects.get_or_create(pk=1)[0]
        if not settings.self_delivery_enabled and not settings.courier_delivery_enabled:
            raise serializers.ValidationError({"delivery_type": "Оформление заказов временно недоступно."})
        if delivery_type == DeliveryType.SELF_DELIVERY and not settings.self_delivery_enabled:
            raise serializers.ValidationError({"delivery_type": "Самовывоз временно недоступен."})
        if delivery_type == DeliveryType.COURIER_DELIVERY and not settings.courier_delivery_enabled:
            raise serializers.ValidationError({"delivery_type": "Доставка курьером временно недоступна."})
        order_data = attrs.get("order_data")
        if not isinstance(order_data, dict):
            raise serializers.ValidationError({"order_data": "Укажите товары заказа."})
        items = OrderItemInputSerializer(
            data=order_data.get("products"), many=True, allow_empty=False
        )
        if not items.is_valid():
            raise serializers.ValidationError({"order_data": items.errors})
        products = Product.objects.prefetch_related("product_image", "external_ids").in_bulk(
            item["product"]["id"] for item in items.validated_data
        )
        lines = []
        subtotal = Decimal(0)
        for item in items.validated_data:
            product = products.get(item["product"]["id"])
            if product is None:
                raise serializers.ValidationError({"order_data": "Товар больше не доступен."})
            price = 0 if product.is_negotiable_price else product.regular_price
            total = Decimal(str(item["quantity"])) * price
            subtotal += total
            lines.append({
                "product": ProductSerializer(product).data,
                "quantity": item["quantity"],
                "total_price": float(total),
            })
        totals = {
            "total_sum": math.floor(subtotal),
            "total_sum_with_delivery": math.floor(subtotal) + attrs.get("delivery_cost", 0),
        }
        for name, value in totals.items():
            try:
                self.fields[name].run_validation(value)
            except serializers.ValidationError as error:
                raise serializers.ValidationError({name: error.detail})
        return {
            **attrs,
            "order_data": {**order_data, "products": lines},
            **totals,
        }
