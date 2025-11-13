from aiogram import Bot, Dispatcher
import asyncio
from config.settings import settings
from handlers.base import BaseHandlers
from handlers.flowers import FlowerHandlers


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    BaseHandlers(dp)
    FlowerHandlers(dp)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
