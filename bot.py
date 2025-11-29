# bot.py
import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from bot.handlers.base import router as base_router
from bot.handlers.flowers import router as flowers_router

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

dp.include_router(base_router)
dp.include_router(flowers_router)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())