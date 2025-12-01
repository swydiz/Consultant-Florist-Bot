from aiogram import types, Dispatcher
from bot.database import database

class FlowerHandlers:
    def __init__(self, dp: Dispatcher):
        dp.callback_query.register(self.show_categories, lambda c: c.data == "show_categories")
        dp.callback_query.register(self.show_flowers, lambda c: c.data.startswith("category_"))
        dp.callback_query.register(self.show_flower, lambda c: c.data.startswith("flower_"))
        dp.callback_query.register(self.add_to_cart, lambda c: c.data.startswith("add_"))

    @staticmethod
    async def show_categories_static(callback: types.CallbackQuery):
        categories = await database.get_categories()
        buttons = []
        for cat in categories:
            buttons.append([types.InlineKeyboardButton(
                text=cat['name'],
                callback_data=f"category_{cat['id']}"
            )])
        buttons.append([types.InlineKeyboardButton(text="Назад", callback_data="back_to_main")])
        await callback.message.edit_text("Выберите категорию:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))
        await callback.answer()

    async def show_categories(self, callback: types.CallbackQuery):
        await self.show_categories_static(callback)

    async def show_flowers(self, callback: types.CallbackQuery):
        cat_id = int(callback.data.split('_')[1])
        flowers = await database.get_flowers_by_category(cat_id)
        buttons = []
        for flower in flowers:
            buttons.append([types.InlineKeyboardButton(
                text=f"{flower['name']} — {flower['price']}₽",
                callback_data=f"flower_{flower['id']}"
            )])
        buttons.append([types.InlineKeyboardButton(text="Назад", callback_data="catalog")])
        await callback.message.edit_text("Выберите цветок:", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=buttons))
        await callback.answer()

    async def show_flower(self, callback: types.CallbackQuery):
        flower_id = int(callback.data.split('_')[1])
        flower = await database.get_flower(flower_id)
        if flower:
            caption = f"**{flower['name']}**\n\nЦена: {flower['price']}₽\nВ наличии: {flower['stock_quantity']} шт."
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{flower_id}")],
                [types.InlineKeyboardButton(text="Назад", callback_data=f"category_{flower['category_id']}")]
            ])
            if flower['photo_url']:
                await callback.message.edit_media(
                    media=types.InputMediaPhoto(media=flower['photo_url'], caption=caption),
                    reply_markup=keyboard
                )
            else:
                await callback.message.edit_text(caption, reply_markup=keyboard, parse_mode="Markdown")
        await callback.answer()

    async def add_to_cart(self, callback: types.CallbackQuery):
        flower_id = int(callback.data.split('_')[1])
        user_id = callback.from_user.id
        flower = await database.get_flower(flower_id)
        if not flower:
            await callback.answer("Цветок не найден", show_alert=True)
            return
        await database.add_order(user_id, flower_id, flower['price'], quantity=1)
        confirm_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="В корзину →", callback_data="cart")],
            [types.InlineKeyboardButton(text="Назад", callback_data=f"flower_{flower_id}")]
        ])
        await callback.message.edit_text(
            f"{flower['name']} добавлен в корзину!",
            reply_markup=confirm_keyboard
        )
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
