from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
from bot.handlers.flowers import get_categories_keyboard

def get_base_keyboard():
    #простая inline-клавиатура 
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Каталог📖", callback_data="catalog")],
            [types.InlineKeyboardButton(text="О нас🤩", callback_data="about")]#добавление кнопки "о нас"
        ]
    )

class BaseHandlers:
    def __init__(self, dp: Dispatcher):
        dp.message.register(self.start_cmd, Command("start"))
        dp.callback_query.register(self.catalog, F.data == "catalog")
        dp.callback_query.register(self.about, F.data == "about")
        dp.callback_query.register(self.back_to_main, F.data == "back_to_main")

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
        
    async def about(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.edit_text(
            "🏪 Наш магазин:\n\n"
            "• Свежие цветы ежедневно\n"
            "• Доставка по городу\n"
            "• Работаем с 9:00 до 21:00",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
                ]
            )
        )
    async def back_to_main(self, callback: types.CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.edit_text(
            "🌸 Добро пожаловать в наш магазинчик цветов!",
            reply_markup=get_base_keyboard()
        )
