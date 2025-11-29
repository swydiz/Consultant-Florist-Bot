from aiogram import types, Dispatcher
from database import AsyncSessionLocal
from models import Category, Flower
from sqlalchemy import select

class FlowerHandlers:
    def __init__(self, dp: Dispatcher):
        dp.callback_query.register(self.show_categories, lambda c: c.data == "show_categories")
        dp.callback_query.register(self.show_flowers, lambda c: c.data.startswith("category_"))
        dp.callback_query.register(self.show_flower, lambda c: c.data.startswith("flower_"))

    @staticmethod
    async def show_categories_static(callback: types.CallbackQuery):
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Category).order_by(Category.id))
            categories = result.scalars().all()

            buttons = []
            for cat in categories:
                buttons.append([types.InlineKeyboardButton(
                    text=cat.name,
                    callback_data=f"category_{cat.id}"
                )])
            buttons.append([types.InlineKeyboardButton(text="Назад", callback_data="back_to_main")])

            await callback.message.edit_text("Выберите категорию:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))
        await callback.answer()

    async def show_categories(self, callback: types.CallbackQuery):
        await self.show_categories_static(callback)

    async def show_flowers(self, callback: types.CallbackQuery):
        cat_id = int(callback.data.split("_")[1])
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Flower).where(Flower.category_id == cat_id))
            flowers = result.scalars().all()

            buttons = []
            for flower in flowers:
                buttons.append([types.InlineKeyboardButton(
                    text=f"{flower.name} — {flower.price}₽",
                    callback_data=f"flower_{flower.id}"
                )])
            buttons.append([types.InlineKeyboardButton(text="Назад", callback_data="catalog")])

            await callback.message.edit_text("Выберите цветок:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))
        await callback.answer()

    async def show_flower(self, callback: types.CallbackQuery):
        flower_id = int(callback.data.split("_")[1])
        async with AsyncSessionLocal() as db:
            flower = await db.get(Flower, flower_id)
            if flower:
                text = f"**{flower.name}**\n\nЦена: {flower.price}₽\nВ наличии: {flower.stock_quantity} шт."
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{flower_id}")],
                    [types.InlineKeyboardButton(text="Назад", callback_data=f"category_{flower.category_id}")]
                ])
                if flower.photo_url:
                    await callback.message.edit_media(
                        media=types.InputMediaPhoto(media=flower.photo_url, caption=text),
                        reply_markup=keyboard
                    )
                else:
                    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        await callback.answer()


'''        await callback.message.edit_text(
            f"Вы выбрали категорию {category_id}. Здесь будут цвета...",
            reply_markup=await get_flowers_keyboard(category_id))'''

"""    async def send_flower(self, callback: types.CallbackQuery, state: FSMContext):
        flower_id = callback.data.split("_")[1]
        # Тут логика карточки цветка
        await callback.message.edit_text(
            f"Карточка цветка id {flower_id}",
            reply_markup=get_flower_keyboard(flower_id)
        )
"""
