from dataclasses import fields

from rest_framework import serializers

from store.serializers import *

from .models import *


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = CartItem
        fields = ["id", "product", "total_price", "quantity"]
