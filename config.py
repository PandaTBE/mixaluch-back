import os

from dotenv import load_dotenv

load_dotenv()

MY_SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
HOST_URL = os.getenv("HOST_URL")

FRONT_DOMAIN = os.getenv("FRONT_DOMAIN")

TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BD_NAME = os.getenv("BD_NAME")
BD_USER = os.getenv("BD_USER")
BD_PASSWORD = os.getenv("BD_PASSWORD")
BD_HOST = os.getenv("BD_HOST")

MY_EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
MY_EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DATABASE_URL = f"postgres://{BD_USER}:{BD_PASSWORD}@{BD_HOST}:5432/{BD_NAME}"

MY_DEBUG = os.getenv("DEBUG")

MY_CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS")
MY_CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS")
