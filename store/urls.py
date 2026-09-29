from django.urls import path, re_path

from . import evotor_views, views

app_name = "store"

urlpatterns = [
    path("api/admin/evotor/stores/", evotor_views.EvotorStoresView.as_view(), name="admin_evotor_stores"),
    re_path(
        r"^api/admin/evotor/stores/(?P<store_id>[0-9A-Fa-f]{8}-(?:[0-9A-Fa-f]{4}-){3}[0-9A-Fa-f]{12})/products/$",
        evotor_views.EvotorProductsView.as_view(), name="admin_evotor_products",
    ),
    path("api/admin/products/", views.AdminProductListView.as_view(), name="admin_products"),
    path("api/v2/products/", views.ProductListV2View.as_view(), name="products_v2"),
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
