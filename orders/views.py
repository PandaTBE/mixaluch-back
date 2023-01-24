from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = []
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_anonymous:
            return serializer.save(user=user)
        return serializer.save(user=None)


class OrderRetriveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderRetriveAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
