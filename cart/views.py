from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CartItem
from .serializers import *


class CartItemListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        """
        Получение товаров в карзине для конкретного пользователя
        """
        user = self.request.user
        return CartItem.objects.filter(user=user)

    def get_serializer_class(self):
        """
        Получение сериализатора в зависимости от типа запроса
        """
        if self.request.method == "GET":
            return CartItemSerializer

        if self.request.method == "POST":
            return CartItemCreateSerializer

    def delete(self, request):
        user = request.user
        CartItem.objects.filter(user=user).delete()
        return Response(status=status.HTTP_200_OK)


class CartItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
