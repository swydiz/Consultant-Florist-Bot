from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.keyboards import get_base_keyboard, get_help_keyboard, get_main_keyboard, get_cart_keyboard
from bot.database import database

class BaseHandlers:
    def __init__(self, dp: Dispatcher):
        dp.message.register(self.start_cmd, Command("start"))
        dp.callback_query.register(self.catalog, lambda c: c.data == "catalog")
        dp.callback_query.register(self.about, lambda c: c.data == "about")
        dp.callback_query.register(self.cart, lambda c: c.data == "cart")
        dp.callback_query.register(self.back_to_main, lambda c: c.data == "back_to_main")
        dp.callback_query.register(self.help_categories, lambda c: c.data == "help_categories")

    async def start_cmd(self, message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Добро пожаловать в наш магазинчик цветов!",
            reply_markup=get_base_keyboard()
        )

    async def catalog(self, callback: types.CallbackQuery):
        await callback.answer()
        from bot.handlers.flowers import FlowerHandlers
        await FlowerHandlers.show_categories_static(callback)

    async def about(self, callback: types.CallbackQuery):
        await callback.answer()
        await callback.message.edit_text(
            "Наш магазин:\n\n• Свежие цветы ежедневно🤗🌺 \n• Доставка по всему городу🚚\n• Работаем с 9:00 до 21:00⏰",
            reply_markup=get_main_keyboard()
        )

    async def cart(self, callback: types.CallbackQuery):
        user_id = callback.from_user.id
        items = await database.get_user_cart(user_id)
        if not items:
            text = "Ваша корзина пока пуста."
        else:
            lines = [f"{item['name']} x {item['quantity']} — {item['price']}₽" for item in items]
            text = "\n".join(lines)
        await callback.answer()
        await callback.message.edit_text(
            text,
            reply_markup=get_cart_keyboard()
        )

    async def back_to_main(self, callback: types.CallbackQuery):
        await callback.answer()
        await callback.message.edit_text(
            "Добро пожаловать в наш магазинчик цветов!",
            reply_markup=get_base_keyboard()
        )

    async def help_categories(self, callback: types.CallbackQuery):
        await callback.answer()
        help_text = "Выберите раздел помощи:"
        await callback.message.edit_text(
            help_text,
            reply_markup=get_help_keyboard()
        )