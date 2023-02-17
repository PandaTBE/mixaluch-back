import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HOST_URL = os.getenv("HOST_URL")
