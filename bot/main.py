import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.handlers.base import BaseHandlers
from bot.handlers.flowers import FlowerHandlers
from bot.config.settings import settings


load_dotenv()
async def main():
    from bot.database import database
    await database.init_db()  #инициализация таблиц при старте
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    print(1)
    BaseHandlers(dp)
    print(2)
    FlowerHandlers(dp)

    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
