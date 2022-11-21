from dataclasses import fields

from rest_framework import serializers

from store.serializers import *

from .models import *


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "total_price", "product", "quantity", "user"]


class CartItemCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemDetailSerializer(CartItemSerializer):
    def create(self, validated_data):
        item = CartItem.objects.create(validated_data)
        return item
