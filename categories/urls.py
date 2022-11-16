from django.urls import path

from . import views

app_name = "categories"


urlpatterns = [path("api/categories/", views.CategoryListView.as_view(), name="Категории")]
