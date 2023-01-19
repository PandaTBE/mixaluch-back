from core import settings
from django.db import models

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
