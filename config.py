import os

from dotenv import load_dotenv

load_dotenv()

MY_SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
HOST_URL = os.getenv("HOST_URL")

FRONT_DOMAIN = os.getenv("FRONT_DOMAIN")
FRONT_PROTOCOL = os.getenv("FRONT_PROTOCOL")

TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

MY_EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
MY_EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

MY_DEBUG = os.getenv("DEBUG")

MY_CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS")
MY_CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS")

EVOTOR_TOKEN = os.getenv("EVOTOR_TOKEN")
