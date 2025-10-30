#Конфигурация и загрузка настроек бота
config.py import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

AI_API_KEY = os.getenv("AI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///flowerbot.db")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
