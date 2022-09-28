from django.contrib import admin

from cart.models import Cart, CartItem


@admin.register(Cart)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__"]


admin.site.register(CartItem)
