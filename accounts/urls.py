from django.urls import include, path, re_path

app_name = "accounts"

urlpatterns = [
    path("api/auth/", include("djoser.urls")),
    re_path(r"^api/auth/", include("djoser.urls.authtoken")),
]
