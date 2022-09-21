from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("api/products/", views.ProductListView.as_view(), name="store_home"),
    path("api/products/<int:pk>/", views.Product.as_view(), name="product"),
    path("api/categories/", views.CategoryListView.as_view(), name="categories"),
]
