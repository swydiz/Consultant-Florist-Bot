from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

class BaseHandlers:
    def __init__(self, dp: Dispatcher):
        dp.message.register(self.start_cmd, Command("start"))
        dp.callback_query.register(self.catalog, lambda c: c.data == "catalog")
        dp.callback_query.register(self.about, lambda c: c.data == "about")
        dp.callback_query.register(self.back_to_main, lambda c: c.data == "back_to_main")

    async def start_cmd(self, message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Добро пожаловать в наш магазинчик цветов!",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Каталог", callback_data="catalog")],
                [types.InlineKeyboardButton(text="О нас", callback_data="about")]
            ])
        )

    async def catalog(self, callback: types.CallbackQuery):
        await callback.answer()
        from bot.handlers.flowers import FlowerHandlers
        await FlowerHandlers.show_categories_static(callback)

    async def about(self, callback: types.CallbackQuery):
        await callback.answer()
        await callback.message.edit_text(
            "Наш магазин:\n\n• Свежие цветы ежедневно\n• Доставка по городу\n• Работаем с 9:00 до 21:00",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
            ])
        )

    async def back_to_main(self, callback: types.CallbackQuery):
        await callback.answer()
        await callback.message.edit_text(
            "Добро пожаловать в наш магазинчик цветов!",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Каталог", callback_data="catalog")],
                [types.InlineKeyboardButton(text="О нас", callback_data="about")]
            ])
        )