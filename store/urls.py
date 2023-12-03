from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("api/products/", views.ProductListView.as_view(), name="store_home"),
    path("api/products/<int:pk>/", views.SingleProduct.as_view(), name="product"),
    path(
        "api/products/popular/",
        views.PopularProducts.as_view(),
        name="main page products",
    ),
    path(
        "api/products/external-id/",
        views.ExternalIdCreateApiView.as_view(),
        name="create_products_external_id",
    ),
    path(
        "api/products/external-id/<int:pk>/",
        views.ExternalIdRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve_products_external_id",
    ),
    path(
        "api/products/image/",
        views.ProductImageCrateApiView.as_view(),
        name="create_product_image",
    ),
    path(
        "api/products/image/<int:pk>/",
        views.ProductImageRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve_products_image",
    ),
]
