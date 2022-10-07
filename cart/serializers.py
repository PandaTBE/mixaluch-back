from dataclasses import fields

from rest_framework import serializers
from store.serializers import *

from .models import *


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "total_price", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "total_price"]
