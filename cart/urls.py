from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("api/cart/", views.CartItemListCreateAPIView.as_view()),
    path("api/cart-item/<int:pk>/", views.CartItemRetrieveUpdateDestroyAPIView.as_view()),
]
