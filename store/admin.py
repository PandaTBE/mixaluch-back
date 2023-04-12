from django.contrib import admin
from django.urls import path
from store.tools.create_feed_file import create_yml_file

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
    change_list_template = "store/CreateYmlFeedButton.html"

    inlines = [ProductImageInline, ProductSpecificationValueInline]
    list_display = ["id", "title"]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('product-feed/', self.get_product_feed),
        ]
        return my_urls + urls

    def get_product_feed(self, request):
        categories = Category.objects.all().values()
        products = Product.objects.all().values()
        response = create_yml_file(categories, products)
        return response