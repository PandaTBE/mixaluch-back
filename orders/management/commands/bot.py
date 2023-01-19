import ast
import os

import requests
from telebot import TeleBot

from core import settings
from django.core.management.base import BaseCommand

# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = "Implemented to Django application telegram bot setup command"

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.infinity_polling()  # Бесконечный цикл бота

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        order_id = call.data.split(",")[0]
        order_status = call.data.split(",")[1]
        admin_token = os.getenv("ADMIN_TOKEN")
        requests.patch(
            f"http://127.0.0.1:8000/api/orders/{order_id}/",
            data={"status": order_status},
            headers={"Authorization": f"Token {admin_token}"},
        )


def message_handler(message, markup):
    bot.send_message("-733292487", message, reply_markup=markup)
