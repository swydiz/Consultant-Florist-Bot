import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from database import AsyncSessionLocal
import os
from dotenv import load_dotenv
from sqlalchemy import text


load_dotenv()
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Привет! База подключена. Напиши /flowers")

@router.message(F.text == "/flowers")
async def flowers(message: Message):
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(text("SELECT name, price FROM flowers"))
            flowers_list = result.fetchall()
            
            if flowers_list:
                text_msg = "Наш каталог:\n\n" + "\n".join(f"• {name} — {price} ₽" for name, price in flowers_list)
            else:
                text_msg = "Каталог пуст"
                
            await message.answer(text_msg)
        except Exception as e:
            await message.answer(f"Ошибка: {e}")

dp.include_router(router)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())