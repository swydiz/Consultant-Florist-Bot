from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_base_keyboard():
    # простая inline-клавиатура с корзиной
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="🛒 Корзина", callback_data="cart")],
            [InlineKeyboardButton(text="🤩 О нас", callback_data="about")],  # добавление кнопки "о нас"
            [InlineKeyboardButton(text="❓ Помощь", callback_data="help_categories")] # добавление кнопки "помощь"
        ]
    )

def get_main_keyboard():
    """(без кнопки 'О нас')"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="🛒 Корзина", callback_data="cart")],
            [InlineKeyboardButton(text="❓ Помощь", callback_data="help_categories")]
        ]
    )


async def get_categories_keyboard():
    """Клавиатура с категориями цветов"""
    from models import Category  # импортируем здесь, чтобы не было циклического импорта
    from database import AsyncSessionLocal
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Category).order_by(Category.id))
        categories = result.scalars().all()
    buttons = []
    for cat in categories:
        buttons.append([
            InlineKeyboardButton(
                text=f"{cat['emoji']} {cat['name']}", 
                callback_data=f"category_{cat['id']}"
            )
        ])
    
    # кнопки помощи
    buttons.append([
        InlineKeyboardButton(text="❓ Помощь", callback_data="help_categories"),
        InlineKeyboardButton(text="⭐ Избранное", callback_data="favorites")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_help_keyboard():
    """Клавиатура для раздела помощи"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Заполнить профиль", callback_data="fill_profile")],
            [InlineKeyboardButton(text="🏠 Изменить адрес доставки", callback_data="change_address")],
            [InlineKeyboardButton(text="📞 Контакты поддержки", callback_data="support_contacts")],
            [InlineKeyboardButton(text="❓ Частые вопросы", callback_data="faq")],
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_main")]
        ]
    )

def get_cart_keyboard():
    """Клавиатура для корзины"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_main")]
        ]
    )