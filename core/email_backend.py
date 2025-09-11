import logging
import smtplib
import socket

from django.conf import settings
from django.core.mail.backends.console import EmailBackend as ConsoleBackend
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend

logger = logging.getLogger(__name__)


class FallbackEmailBackend(SMTPBackend):
    """
    Email backend с fallback на консольный вывод при ошибках SMTP
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.console_backend = ConsoleBackend(*args, **kwargs)

    def send_messages(self, email_messages):
        """
        Пытается отправить через SMTP, при ошибке выводит в консоль
        """
        if not email_messages:
            return 0

        try:
            logger.info(f"Попытка отправки {len(email_messages)} сообщений через SMTP")
            return super().send_messages(email_messages)

        except (socket.error, smtplib.SMTPException, OSError) as e:
            logger.warning(
                f"SMTP недоступен: {str(e)}. Переключаемся на консольный вывод"
            )

            # Fallback на консольный backend
            return self.console_backend.send_messages(email_messages)

        except Exception as e:
            logger.error(f"Неожиданная ошибка при отправке email: {str(e)}")

            # В случае любой другой ошибки тоже используем консоль
            return self.console_backend.send_messages(email_messages)
