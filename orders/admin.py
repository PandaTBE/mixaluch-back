from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.html import format_html

from orders.models import Order
from orders.notifications import send_order_notifications


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__", "user", "status"]
    readonly_fields = ["resend_button"]

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<int:order_id>/resend/",
                self.admin_site.admin_view(self.resend_notifications),
                name="orders_order_resend",
            ),
        ]
        return custom + urls

    def resend_notifications(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        send_order_notifications(order)
        self.message_user(request, f"Уведомления для заказа #{order_id} отправлены.", messages.SUCCESS)
        return redirect(reverse("admin:orders_order_change", args=[order_id]))

    def resend_button(self, obj):
        if obj.pk:
            url = reverse("admin:orders_order_resend", args=[obj.pk])
            return format_html(
                '<a class="button" href="{}">Отправить в Telegram и на почту</a>',
                url,
            )
        return "—"

    resend_button.short_description = "Переотправка уведомлений"
