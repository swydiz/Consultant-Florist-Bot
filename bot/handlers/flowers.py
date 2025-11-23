from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Dispatcher


FLOWERS_DATA = {
    1: [
        {"id": 101, "name": "🌹 Красная роза", "price": 150, "description": "Классическая красная роза - символ любви и страсти", "care": "Меняйте воду каждые 2 дня, обрезайте стебли под углом"},
        {"id": 102, "name": "🌷 Розовая роза", "price": 140, "description": "Нежная розовая роза выражает восхищение и благодарность", "care": "Держите в прохладном месте, избегайте прямых солнечных лучей"},
        {"id": 103, "name": "💛 Желтая роза", "price": 130, "description": "Солнечная желтая роза символизирует дружбу и радость", "care": "Добавьте в воду специальную подкормку для цветов"}
    ],
    2: [
        {"id": 201, "name": "🌷 Красный тюльпан", "price": 120, "description": "Яркий красный тюльпан - признание в любви", "care": "Не ставьте рядом с фруктами, выделяющими этилен"},
        {"id": 202, "name": "💜 Фиолетовый тюльпан", "price": 125, "description": "Фиолетовый тюльпан символизирует роскошь и королевскую власть", "care": "Идеальная температура +18-20°C"}
    ],
    3: [
        {"id": 301, "name": "🌺 Красный георгин", "price": 180, "description": "Пышный красный георгин с множеством лепестков", "care": "Требует много воды, следите за влажностью почвы"},
        {"id": 302, "name": "🌸 Розовый георгин", "price": 170, "description": "Нежный розовый георгин с градиентными лепестками", "care": "Защищайте от сильного ветра и дождя"}
    ],
    4: [
        {"id": 401, "name": "🌺 Белый пион", "price": 200, "description": "Пушистый белый пион - символ богатства и чести", "care": "Очень чувствителен к сквознякам"},
        {"id": 402, "name": "🌷 Розовый пион", "price": 190, "description": "Нежно-розовый пион с насыщенным ароматом", "care": "Меняйте воду ежедневно"}
    ],
    5: [
        {"id": 501, "name": "💮 Белый лотос", "price": 300, "description": "Священный лотос - символ чистоты и просветления", "care": "Требует особых условий, только для опытных флористов"}
    ],
    6: [
        {"id": 601, "name": "🏵️ Коралловый пион", "price": 220, "description": "Редкий коралловый пион с уникальным оттенком", "care": "Стабильная температура, без резких перепадов"}
    ]
}

CATEGORIES = [
    {"id": 1, "name": "🌹 Розы", "emoji": "🌹", "description": "Королева цветов с богатой палитрой оттенков"},
    {"id": 2, "name": "🌷 Тюльпаны", "emoji": "🌷", "description": "Весенние цветы с элегантной формой"},
    {"id": 3, "name": "🌺 Георгины", "emoji": "🌺", "description": "Пышные цветы с множеством лепестков"},
    {"id": 4, "name": "🌸 Пионы", "emoji": "🌸", "description": "Пушистые и ароматные весенние цветы"},
    {"id": 5, "name": "💮 Лотосы", "emoji": "💮", "description": "Водные цветы с духовным значением"},
    {"id": 6, "name": "🏵️ Пионы махровые", "emoji": "🏵️", "description": "Особые сорта с густыми лепестками"}
]

async def get_categories_keyboard() -> types.InlineKeyboardMarkup:
    """Клавиатура с категориями цветов"""
    buttons = []
    for cat in CATEGORIES:
        buttons.append([
            types.InlineKeyboardButton(
                text=f"{cat['emoji']} {cat['name']}", 
                callback_data=f"category_{cat['id']}"
            )
        ])
    
    # Добавляем кнопку помощи
    buttons.append([
        types.InlineKeyboardButton(text="❓ Помощь", callback_data="help_categories"),
        types.InlineKeyboardButton(text="⭐ Избранное", callback_data="favorites")
    ])
    
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

async def get_flowers_keyboard(category_id: int) -> types.InlineKeyboardMarkup:
    """Клавиатура с цветами выбранной категории"""
    flowers = FLOWERS_DATA.get(int(category_id), [])
    buttons = []
    
    for flower in flowers:
        buttons.append([
            types.InlineKeyboardButton(
                text=f"{flower['name']} - {flower['price']}₽", 
                callback_data=f"flower_{flower['id']}"
            )
        ])
    
    # Добавляем навигационные кнопки
    buttons.extend([
        [types.InlineKeyboardButton(text="◀️ Назад к категориям", callback_data="back_to_categories")],
        [types.InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

async def get_flower_keyboard(flower_id: int) -> types.InlineKeyboardMarkup:
    """Клавиатура для карточки цветка"""
    buttons = [
        [
            types.InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data=f"add_to_cart_{flower_id}"),
            types.InlineKeyboardButton(text="❤️ В избранное", callback_data=f"add_favorite_{flower_id}")
        ],
        [
            types.InlineKeyboardButton(text="📸 Фото цветка", callback_data=f"photo_{flower_id}"),
            types.InlineKeyboardButton(text="💬 Консультация", callback_data=f"consult_{flower_id}")
        ],
        [
            types.InlineKeyboardButton(text="◀️ Назад к цветам", callback_data=f"back_to_flowers_{flower_id//100}"),
            types.InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")
        ]
    ]
    
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


class FlowerHandlers:
    def __init__(self, dp):
        dp.callback_query.register(self.send_categories, F.data.startswith("category_"))
        
    async def send_categories(self, callback: types.CallbackQuery, state: FSMContext):
        category_id = callback.data.split("_")[1]
        category = next((cat for cat in CATEGORIES if str(cat["id"]) == category_id), None)
        
        if category:
            await callback.message.edit_text(
                f"**{category['emoji']} {category['name']}**\n\n"
                f"{category['description']}\n\n"
                f"*Выберите конкретный цветок из этой категории:*",
                parse_mode="Markdown",
                reply_markup=await get_flowers_keyboard(category_id)
            )
        await callback.answer()

    async def send_flower(self, callback: types.CallbackQuery, state: FSMContext):
        """Показать карточку цветка"""
        flower_id = int(callback.data.split("_")[1])
        
        # Находим цветок во всех категориях
        flower = None
        category_id = 0
        for cat_id, flowers in FLOWERS_DATA.items():
            for f in flowers:
                if f["id"] == flower_id:
                    flower = f
                    category_id = cat_id
                    break
        
        if flower:
            flower_text = (
                f"**{flower['name']}**\n\n"
                f"💵 **Цена:** {flower['price']}₽\n"
                f"📝 **Описание:** {flower['description']}\n"
                f"🌱 **Уход:** {flower['care']}\n\n"
                f"*Вы можете добавить цветок в корзину или получить консультацию флориста*"
            )
            
            await callback.message.edit_text(
                flower_text,
                parse_mode="Markdown",
                reply_markup=await get_flower_keyboard(flower_id)
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