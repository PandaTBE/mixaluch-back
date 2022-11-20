from core import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from store.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)
    quantity = models.FloatField(default=1)

    def __str__(self):
        return f"{self.user.email} {self.product.title}"


@receiver(pre_save, sender=CartItem)
def correct_price(sender, instance, **kwargs):
    """
    Сигнал срабатывает при сохранении CartItem
    """
    product = Product.objects.get(id=instance.product.id)
    instance.total_price = instance.quantity * product.regular_price
