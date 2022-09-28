from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from store.models import Product

from .models import Cart, CartItem
from .serializers import *


class CartRetriveApiView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartSerializer(instance=cart)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        cart = Cart.objects.get(user=user)
        product = Product.objects.get(id=data.get("product"))
        quantity = data.get("quantity")
        cart_item = CartItem(cart=cart, product=product, quantity=quantity)
        cart_item.save()

        cart_items = CartItem.objects.filter(cart=cart.id)
        total_price = 0
        for item in cart_items:
            total_price += item.total_price
            cart.total_price = total_price
        cart.save()

        return Response({"success": "Items Added to your cart"})

    def patch(self, request):
        data = request.data
        cart_item = CartItem.objects.get(id=data.get("id"))
        quantity = data.get("quantity")

        cart_item.quantity = quantity
        cart_item.save()
        return Response({"success": "Item updated"})

    def delete(self, request):
        user = request.user
        data = request.data

        cart_item = CartItem.objects.get(id=data.get("id"))
        cart_item.delete()
        cart = Cart.objects.get(user=user)
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)
