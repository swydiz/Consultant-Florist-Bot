from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_base_keyboard():
    #простая inline-клавиатура 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Каталог📖", callback_data="catalog")],
            [InlineKeyboardButton(text="О нас🤩", callback_data="about")]#добавление кнопки "о нас"
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
    
    # Добавляем кнопку помощи
    buttons.append([
        InlineKeyboardButton(text="❓ Помощь", callback_data="help_categories"),
        InlineKeyboardButton(text="⭐ Избранное", callback_data="favorites")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
