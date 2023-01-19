from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from core import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.management.commands.bot import Command, message_handler

# Create your models here.


class OrderStatus(models.TextChoices):
    IN_PROCESS = "IN_PROCESS", "В обработке"
    ACCEPTED = "ACCEPTED", "Принят"
    COLLECTED = "COLLECTED", "Собран"
    IN_DELIVERY = "IN_DELIVERY", "В доставке"
    COMPLETED = "COMPLETED", "Выполнен"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255, null=True, default=None, blank=True)
    phone_number = models.CharField(max_length=30, null=False, blank=False)
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.IN_PROCESS)
    order_data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.email} - {self.name}"


@receiver(post_save, sender=Order)
def correct_price(sender, instance, created, **kwargs):
    """
    Сигнал срабатывает при сохранении CartItem
    """
    if created:

        message_handler(123, gen_markup(instance.id))


def gen_markup(order_id):

    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton(
            order_id,
            callback_data=f"{order_id},COMPLETED",
        ),
        InlineKeyboardButton("No", callback_data="cb_no"),
    )
    return markup
