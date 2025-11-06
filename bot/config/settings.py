import os
from dotenv import load_dotenv

load_dotenv("settings.env")
print("DEBUG TOKEN:", os.getenv("BOT_TOKEN"))

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHANNEL_URL = os.getenv("CHANNEL_URL")
    ADMIN_IDS = os.getenv("ADMIN_IDS", "")

settings = Settings()