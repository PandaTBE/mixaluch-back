import logging
import threading
import time
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail

from config import NOTIFICATION_EMAILS

logger = logging.getLogger(__name__)


def send_telegram_notification(instance) -> bool:
    try:
        from orders.models import create_message, gen_markup
        from orders.management.commands.bot import message_handler

        message_handler(create_message(instance), gen_markup(instance.id))
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки уведомления в Telegram для заказа #{instance.id}: {e}")
        return False


def _send_email_async(subject, html_message, recipient_list):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            send_mail(
                subject=subject,
                message="",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Email отправлен на {recipient_list} с попытки {attempt + 1}")
            return True
        except SMTPException as e:
            logger.warning(f"SMTP ошибка попытка {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                logger.error(f"Не удалось отправить email после {max_retries} попыток")
        except Exception as e:
            logger.error(f"Критическая ошибка при отправке email: {e}")
            break
    return False


def send_email_notification(instance) -> bool:
    if not NOTIFICATION_EMAILS:
        return False

    recipients = [e.strip() for e in NOTIFICATION_EMAILS.split(",") if e.strip()]
    if not recipients:
        return False

    try:
        from orders.models import create_message

        subject = f"Новый заказ #{instance.id}"
        html_message = create_message(instance).replace("\n", "<br>")

        thread = threading.Thread(
            target=_send_email_async,
            args=(subject, html_message, recipients),
            daemon=True,
        )
        thread.start()
        return True
    except Exception as e:
        logger.error(f"Ошибка запуска email-уведомления для заказа #{instance.id}: {e}")
        return False


def send_order_notifications(instance):
    send_telegram_notification(instance)
    send_email_notification(instance)
