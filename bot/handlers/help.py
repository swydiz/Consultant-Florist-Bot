from aiogram import types, Dispatcher
from bot.database import database

class HelpHandlers:
    def __init__(self, dp: Dispatcher):
        dp.callback_query.register(self.fill_profile, lambda c: c.data == "fill_profile")
        dp.callback_query.register(self.change_address, lambda c: c.data == "change_address")
        dp.callback_query.register(self.support_contacts, lambda c: c.data == "support_contacts")
        dp.callback_query.register(self.faq, lambda c: c.data == "faq")

    async def fill_profile(self, callback: types.CallbackQuery):
        await callback.answer()
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Назад", callback_data="help_categories")]
        ])
        
        await callback.message.edit_text(
            "🩺 <b>Укажите ваши аллергии или непереносимости:</b>\n\n"
            "Напишите продукты, на которые у вас аллергия.\n"
            "<i>Пример: орехи, мед, цитрусовые</i>\n\n"
            "Если аллергий нет, напишите 'нет'.",
            reply_markup=keyboard,
            parse_mode="HTML"
        )


    async def change_address(self, callback: types.CallbackQuery):
        await callback.answer()
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="Назад", callback_data="help_categories")]
        ])
        await callback.message.edit_text(
            "📍 Введите новый адрес доставки:\n\n"
            "<i>Пример: г. Москва, ул. Ленина, д. 10, кв. 25</i>\n\n",
            reply_markup=keyboard,
            parse_mode="HTML"
        )


    async def support_contacts(self, callback: types.CallbackQuery):
        await callback.answer()
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Назад", callback_data="help_categories")]
            ])        
        await callback.message.edit_text(
            "Наши контакты: \n\n• по вопросам доставки: 8-800-555-55-55 \n• менеджер по заказам: 8-905-125-65-37 \n• проблемы с профилем: 8-920-345-76-43", 
            reply_markup = keyboard
        )


    async def faq(self, callback: types.CallbackQuery):
        await callback.answer()
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Назад", callback_data="help_categories")]
            ]) 
        await callback.message.edit_text(
            "• Как быстро я получу свой заказ? \n  - Мы будем уведомлять о вас о статусе вашего заказа, но гарантируем, что вы получите его в течении 2-х суток или ранее. Если же заказ не будет доставлен в эти сроки, мы подарим вам промокод и вернем деньги. \n• Если я не могу забрать заказ, что делать? \n  -Ничего страшного. В таком случае заказ может забрать любое доверенное лицо, оибо же вы можете попросить курьера оставить ваш букет у двери.", 
            reply_markup = keyboard        
        )

