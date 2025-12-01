import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.BOT_TOKEN = os.getenv('BOT_TOKEN')
        self.DB_FILENAME = os.getenv('DB_FILENAME', 'flowerbot.db')
        self.CHANNEL_URL = os.getenv('CHANNEL_URL')
        # Строка с id может быть через запятую, превратить в список интеджеров
        admin_ids = os.getenv('ADMIN_IDS')
        if admin_ids:
            self.ADMIN_IDS = [int(x) for x in admin_ids.split(',') if x.strip().isdigit()]
        else:
            self.ADMIN_IDS = []

settings = Settings()