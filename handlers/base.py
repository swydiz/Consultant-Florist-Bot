from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
from handlers.flowers import get_categories_keyboard

def get_base_keyboard():
    #простая inline-клавиатура 
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Каталог", callback_data="catalog")]
        ]
    )

class BaseHandlers:
    def __init__(self, dp: Dispatcher):
        dp.message.register(self.start_cmd, Command("start"))
        dp.callback_query.register(self.catalog, F.data == "catalog")

    async def start_cmd(self, message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "🌸 Добро пожаловать в наш магазинчик цветов!",
            reply_markup=get_base_keyboard()
        )

    async def catalog(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.answer()
        categories_keyboard = await get_categories_keyboard()

        await callback.message.edit_text(
        "🌷 Выберите категорию цветов:",
        reply_markup=categories_keyboard
    )
