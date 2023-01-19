from django.contrib import admin
from orders.models import Order

# Register your models here.


@admin.register(Order)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__", "user", "status"]
