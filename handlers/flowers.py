from aiogram import types, F
from aiogram.fsm.context import FSMContext

async def get_categories_keyboard():
    categories = [
        {"id": 1, "name": "Розы"},
        {"id": 2, "name": "Тюльпаны"},
        {"id": 3, "name": "Георгины"},
    ]
    buttons = [
        [types.InlineKeyboardButton(text=cat["name"], callback_data=f"category_{cat['id']}")]
        for cat in categories
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


class FlowerHandlers:
    def __init__(self, dp):
        dp.callback_query.register(self.send_categories, F.data.startswith("category_"))
        
    async def send_categories(self, callback: types.CallbackQuery, state: FSMContext):
        category_id = callback.data.split("_")[1]

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