from aiogram import Bot, Dispatcher
import asyncio
import os
from dotenv import load_dotenv

from bot.handlers.base import BaseHandlers
from bot.handlers.flowers import FlowerHandlers

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    BaseHandlers(dp)
    FlowerHandlers(dp)
    
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())