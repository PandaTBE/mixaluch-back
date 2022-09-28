from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("api/cart/", views.CartRetriveApiView.as_view()),
]
