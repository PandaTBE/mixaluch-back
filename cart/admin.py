from cart.models import CartItem
from django.contrib import admin


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__", "quantity", "total_price"]
