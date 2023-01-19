from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("api/orders/", views.OrderListCreateAPIView.as_view()),
    path("api/orders/<int:pk>/", views.OrderRetriveUpdateAPIView.as_view()),
]
