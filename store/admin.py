import logging

from django.conf import settings
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from categories.models import Category
from store.tools.change_price_by_evotor import change_price_by_evotor
from store.tools.get_ya_business_feed import get_ya_business_feed
from store.tools.get_ya_webmaster_feed import get_ya_webmaster_feed

from .models import (
    Product,
    ProductExternalId,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
)

logger = logging.getLogger(__name__)

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


class ProductExternalIdInline(admin.TabularInline):
    model = ProductExternalId


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = "store/CreateYmlFeedButtons.html"

    inlines = [
        ProductImageInline,
        ProductSpecificationValueInline,
        ProductExternalIdInline,
    ]
    list_display = ["id", "title"]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("change-price-by-evotor/", self.price_by_evotor),
            path("product-feed-ya-business/", self.ya_business_feed),
            path("product-feed-ya-webmaster/", self.ya_webmaster_feed),
            path("test-email/", self.test_email),
        ]
        return my_urls + urls

    def price_by_evotor(self, request):
        """
        Изменение цен на основе данных Эвотора
        """
        products = Product.objects.all()
        response = change_price_by_evotor(products)
        return response

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

    @method_decorator(csrf_exempt)
    def test_email(self, request):
        """
        Тестовая отправка email для проверки настроек
        """
        try:
            logger.info("Начинаем отправку тестового email")

            if not settings.EMAIL_HOST_USER:
                return JsonResponse(
                    {"success": False, "message": "EMAIL_HOST_USER не настроен"}
                )

            send_mail(
                subject="Тестовое письмо от Django",
                message="Это тестовое сообщение для проверки работы email на сервере.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            logger.info("Тестовый email успешно отправлен")
            return JsonResponse(
                {"success": True, "message": "Тестовое письмо успешно отправлено!"}
            )

        except Exception as e:
            logger.error(f"Ошибка отправки тестового email: {str(e)}")
            return JsonResponse(
                {"success": False, "message": f"Ошибка отправки email: {str(e)}"}
            )
