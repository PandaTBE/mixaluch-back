from django.urls import path

from . import views

app_name = "categories"


urlpatterns = [
    path("api/categories/", views.CategoryListView.as_view(), name="Категории"),
    path("api/categories/main/", views.MainCategoriesListView.as_view(), name="Основные категории"),
]
