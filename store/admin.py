from django.contrib import admin
from django.urls import path
from store.tools.get_ya_business_feed import get_ya_business_feed
from store.tools.get_ya_webmaster_feed import get_ya_webmaster_feed

from categories.models import Category

from .models import (
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)
"""
для одновременного заполнения типа продукта и спецификации используем inline
"""


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductSpecificationInline]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = "store/CreateYmlFeedButtons.html"

    inlines = [ProductImageInline, ProductSpecificationValueInline]
    list_display = ["id", "title"]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('product-feed-ya-business/', self.ya_business_feed),
            path('product-feed-ya-webmaster/', self.ya_webmaster_feed),
        ]
        return my_urls + urls

    def ya_business_feed(self, request):
        """
        Получение списка товаров для Я.Бизнеса
        """
        categories = Category.objects.all().values()
        products = Product.objects.all().values()
        response = get_ya_business_feed(categories, products)
        return response

    def ya_webmaster_feed(self, request):
        """
        Получение списка товаров для Я.Вебмастера
        """
        categories = Category.objects.all().values()
        products = Product.objects.all().values()
        response = get_ya_webmaster_feed(categories, products)
        return response