import logging
import threading

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


def send_email_async(subject, message, from_email, recipient_list):
    """
    Асинхронная отправка email в отдельном потоке с retry логикой
    """
    import time
    from smtplib import SMTPException

    max_retries = 3
    base_delay = 1

    for attempt in range(max_retries):
        try:
            logger.info(
                f"Попытка {attempt + 1} асинхронной отправки email для {recipient_list}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )

            logger.info(f"Email успешно отправлен асинхронно с попытки {attempt + 1}")
            return True

        except SMTPException as e:
            logger.warning(f"SMTP ошибка на попытке {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                delay = base_delay * (2**attempt)  # Экспоненциальная задержка
                logger.info(f"Ожидание {delay} сек перед следующей попыткой")
                time.sleep(delay)
            else:
                logger.error(f"Не удалось отправить email после {max_retries} попыток")

        except Exception as e:
            logger.error(f"Критическая ошибка при отправке email: {str(e)}")
            break

    return False


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
        Тестовая отправка email для проверки настроек (асинхронно)
        """
        try:
            logger.info("Запуск тестовой отправки email")

            if not settings.EMAIL_HOST_USER:
                return JsonResponse(
                    {"success": False, "message": "EMAIL_HOST_USER не настроен"}
                )

            # Запускаем отправку email в отдельном потоке
            email_thread = threading.Thread(
                target=send_email_async,
                args=(
                    "Тестовое письмо от Django",
                    "Это тестовое сообщение для проверки работы email на сервере.",
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                ),
            )
            email_thread.daemon = (
                True  # Поток завершится при завершении основного процесса
            )
            email_thread.start()

            logger.info("Email отправка запущена в фоновом режиме")
            return JsonResponse(
                {
                    "success": True,
                    "message": "Тестовое письмо отправляется в фоновом режиме. Проверьте почту через 1-2 минуты.",
                }
            )

        except Exception as e:
            logger.error(f"Ошибка запуска тестового email: {str(e)}")
            return JsonResponse(
                {
                    "success": False,
                    "message": f"Ошибка запуска отправки email: {str(e)}",
                }
            )
