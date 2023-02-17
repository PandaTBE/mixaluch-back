import os
import re

import requests
from django.core.management.base import BaseCommand
from telebot import TeleBot

from config import ADMIN_TOKEN, HOST_URL, TELEGRAM_BOT_API_KEY, TELEGRAM_CHAT_ID

# Объявление переменной бота
bot = TeleBot(TELEGRAM_BOT_API_KEY, threaded=False)
chat_id = TELEGRAM_CHAT_ID

ORDER_STATUS_NAMES_MAP = {
    "IN_PROCESS": "В обработке",
    "ACCEPTED": "Принят",
    "COLLECTED": "Собран",
    "IN_DELIVERY": "В доставке",
    "COMPLETED": "Выполнен",
}


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

    status_regexp = "Статус заказа:  \D+(?=Заказчик)"

    order_id = call.data.split(",")[0]
    order_status = call.data.split(",")[1]
    admin_token = ADMIN_TOKEN

    message_text = call.message.text

    new_message = re.sub(
        status_regexp, f"Статус заказа:  {ORDER_STATUS_NAMES_MAP.get(order_status, '?')}\n\n", message_text
    )

    requests.patch(
        f"{HOST_URL}/api/orders/{order_id}/",
        data={"status": order_status},
        headers={"Authorization": f"Token {admin_token}"},
    )
    bot.edit_message_text(
        chat_id=chat_id,
        text=new_message,
        message_id=call.message.message_id,
        reply_markup=call.message.reply_markup,
        parse_mode="html",
    )


def message_handler(message, markup):
    bot.send_message(chat_id, message, reply_markup=markup, parse_mode="html")
