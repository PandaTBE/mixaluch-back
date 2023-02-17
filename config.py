import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HOST_URL = os.getenv("HOST_URL")
SQL_BD_NAME = os.getenv("SQL_BD_NAME")
SQL_BD_USER = os.getenv("SQL_BD_USER")
SQL_BD_PASSWORD = os.getenv("SQL_BD_PASSWORD")
SQL_BD_HOST = os.getenv("SQL_BD_HOST")
FRONT_DOMAIN = os.getenv("FRONT_DOMAIN")
