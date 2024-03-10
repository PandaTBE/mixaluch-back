import datetime
import math

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from cart.models import CartItem
from core import settings
from orders.management.commands.bot import message_handler
from store.models import PRODUCT_UNIT_MAP

DEFAULT_DELIVERY_DATE = "AS_SOON_AS_POSSIBLE"


class OrderStatus(models.TextChoices):
    IN_PROCESS = "IN_PROCESS", "В обработке"
    ACCEPTED = "ACCEPTED", "Принят"
    COLLECTED = "COLLECTED", "Собран"
    IN_DELIVERY = "IN_DELIVERY", "В доставке"
    COMPLETED = "COMPLETED", "Выполнен"


ORDER_STATUS_NAMES_MAP = {
    "IN_PROCESS": "В обработке",
    "ACCEPTED": "Принят",
    "COLLECTED": "Собран",
    "IN_DELIVERY": "В доставке",
    "COMPLETED": "Выполнен",
}


class DeliveryType(models.TextChoices):
    SELF_DELIVERY = (
        "SELF_DELIVERY",
        "Самовывоз",
    )
    COURIER_DELIVERY = "COURIER_DELIVERY", "Курьером"


DELIVERY_TYPE_NAMES_MAP = {"SELF_DELIVERY": "Самовывоз", "COURIER_DELIVERY": "Курьером"}


class PaymentType(models.TextChoices):
    CASH_PAYMENT = "CASH_PAYMENT", "Наличными"
    CARD_PAYMENT = "CARD_PAYMENT", "Картой"


PAYMENT_TYPE_NAMES_MAP = {
    "CASH_PAYMENT": "Наличными",
    "CARD_PAYMENT": "Картой",
}


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30, null=False, blank=False)
    status = models.CharField(
        max_length=30, choices=OrderStatus.choices, default=OrderStatus.IN_PROCESS
    )
    comment = models.CharField(blank=True, default="", max_length=3000)
    address = models.CharField(blank=True, default="", max_length=1000)
    delivery_type = models.CharField(
        max_length=50,
        choices=DeliveryType.choices,
        default=DeliveryType.COURIER_DELIVERY,
    )
    payment_type = models.CharField(
        max_length=50, choices=PaymentType.choices, default=PaymentType.CARD_PAYMENT
    )
    delivery_date = models.CharField(max_length=64, default=DEFAULT_DELIVERY_DATE)
    order_data = models.JSONField(default=dict)
    delivery_cost = models.PositiveIntegerField(default=0)
    total_sum = models.PositiveIntegerField(default=0)
    total_sum_with_delivery = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-{self.phone_number}"


@receiver(pre_save, sender=Order)
def clear_cart(sender, instance, **kwargs):
    """
    Сигнал срабатывает перед сохранение заказа и очищает корзину
    """
    user = instance.user

    if user is not None:
        CartItem.objects.filter(user=user).delete()


@receiver(post_save, sender=Order)
def correct_price(sender, instance, created, **kwargs):
    """
    Сигнал срабатывает после сохранении Order. Отправляет сообщение в телеграмм
    """
    if created:
        message_handler(create_message(instance), gen_markup(instance.id))


new_line = "\n"


def create_message(instance):

    return f"\
{format_order_data('Номер заказа', instance.id)}\
{format_order_data('Статус заказа', ORDER_STATUS_NAMES_MAP.get(instance.status, '?'))}\
{format_order_data('Заказчик', instance.name)}\
{format_order_data('Телефон', instance.phone_number)}\
{format_order_data('Тип доставки', DELIVERY_TYPE_NAMES_MAP.get(instance.delivery_type, '?'))}\
{format_order_data('Адрес доставки', instance.address)}\
{format_order_data('Дата и время доставки', format_delivery_date(instance.delivery_date))}\
{format_order_data('Расчет', PAYMENT_TYPE_NAMES_MAP.get(instance.payment_type, '?'))}\
{format_order_data('Комментарий', instance.comment)}\
{format_order_data('Стоимость доставки', f'{instance.delivery_cost} руб.')}\
{format_order_data('Итого', f'{instance.total_sum_with_delivery} руб.')}\
{format_order_data('Заказ', format_order_products(instance.order_data.get('products', [])))}"


def format_delivery_date(delivery_date):
    try:
        datetime_obj = datetime.datetime.fromisoformat(delivery_date)
        datetime_str = datetime_obj.strftime("%d-%m-%Y, %H:%M %Z")
        return datetime_str
    except ValueError:
        return "Как можно скорее"


def format_order_products(products):
    tab = "    "

    result = "\n"
    for product in products:
        unit = product["product"].get("unit", "")
        translated_unit = PRODUCT_UNIT_MAP.get(unit, "")
        value = f"\
{tab}{format_title('Товар')}   {product['product']['title']}{new_line}\
{tab}{format_title('Цена')}    {product['product']['regular_price']} руб.{new_line}\
{tab}{format_title('Кол-во')}  {product['quantity']} {translated_unit}.{new_line}\
{tab}{format_title('Сумма')}   {math.floor(product['quantity'] * product['product']['regular_price'])} руб.{new_line * 2}"

        result += value
    return result


def format_order_data(title, value):
    return f"{format_title(title)}  {value}{new_line * 2}"


def format_title(title):
    return f"<b><i>{title}:</i></b>"


def gen_markup(order_id):

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton(
            "В обработке",
            callback_data=f"{order_id},IN_PROCESS",
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Принят",
            callback_data=f"{order_id},ACCEPTED",
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Собран",
            callback_data=f"{order_id},COLLECTED",
        )
    )
    markup.add(
        InlineKeyboardButton(
            "В доставке",
            callback_data=f"{order_id},IN_DELIVERY",
        )
    )
    markup.add(
        InlineKeyboardButton(
            "Выполнен",
            callback_data=f"{order_id},COMPLETED",
        ),
    )
    return markup
