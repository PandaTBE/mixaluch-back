from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from core import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.management.commands.bot import message_handler

# Create your models here.


class OrderStatus(models.TextChoices):
    IN_PROCESS = "IN_PROCESS", "В обработке"
    ACCEPTED = "ACCEPTED", "Принят"
    COLLECTED = "COLLECTED", "Собран"
    IN_DELIVERY = "IN_DELIVERY", "В доставке"
    COMPLETED = "COMPLETED", "Выполнен"


class DeliveryType(models.TextChoices):
    SELF_DELIVERY = (
        "SELF_DELIVERY",
        "Самовывоз",
    )
    COURIER_DELIVERY = "COURIER_DELIVERY", "Курьером"


class PaymentType(models.TextChoices):
    CASH_PAYMENT = "CASH_PAYMENT", "Наличными"
    CARD_PAYMENT = "CARD_PAYMENT", "Картой"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30, null=False, blank=False)
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.IN_PROCESS)
    comment = models.CharField(blank=True, default="", max_length=3000)
    address = models.CharField(blank=True, default="", max_length=1000)
    delivery_type = models.CharField(
        max_length=50, choices=DeliveryType.choices, default=DeliveryType.COURIER_DELIVERY
    )
    payment_type = models.CharField(max_length=50, choices=PaymentType.choices, default=PaymentType.CARD_PAYMENT)
    order_data = models.JSONField(default=dict)
    delivery_cost = models.PositiveIntegerField(default=0)
    products_total = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}-{self.phone_number}"


@receiver(post_save, sender=Order)
def correct_price(sender, instance, created, **kwargs):
    """
    Сигнал срабатывает при сохранении CartItem
    """
    if created:

        message_handler(create_message(instance), gen_markup(instance.id))


def create_message(instance):
    return f"Статус заказа: {instance.status}\n\
Имя: {instance.name}\n\
Телефон: {instance.phone_number}\n\
Адрес: {instance.address}\
"


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
            "Заавершен",
            callback_data=f"{order_id},COMPLETED",
        ),
    )
    return markup
