import aiosqlite
from bot.config.settings import settings

DB_FILENAME = settings.DB_FILENAME

async def init_db():
    async with aiosqlite.connect(DB_FILENAME) as db:
        # Включаем внешние ключи в SQLite
        await db.execute('PRAGMA foreign_keys = ON;')

        await db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY,           -- BIGINT → INTEGER
            username   VARCHAR(100),
            first_name VARCHAR(100),
            last_name  VARCHAR(100),
            allergy    TEXT,
            role       VARCHAR(20) DEFAULT 'user'
        );

        CREATE TABLE IF NOT EXISTS categories (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        VARCHAR(100) NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS flowers (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            name           VARCHAR(150) NOT NULL,
            price          NUMERIC(10,2) NOT NULL,   -- для денег лучше NUMERIC, а не REAL [web:31][web:34]
            photo_url      TEXT NOT NULL,
            category_id    INTEGER,
            stock_quantity INTEGER DEFAULT 999,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );

        CREATE TABLE IF NOT EXISTS orders (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id        INTEGER,
            flower_id      INTEGER,
            quantity       INTEGER DEFAULT 1,
            price_at_order NUMERIC(10,2) NOT NULL,
            status         VARCHAR(20) DEFAULT 'pending',
            FOREIGN KEY (user_id)  REFERENCES users(id),
            FOREIGN KEY (flower_id) REFERENCES flowers(id)
        );

        CREATE TABLE IF NOT EXISTS messages (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chat_id INTEGER,
            content TEXT NOT NULL,
            role    VARCHAR(10) NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            CHECK (role IN ('user','bot'))
        );
        ''')

        # Стартовые данные (выполнить один раз; можно добавить защиту, чтобы не дублировать)
        await db.executescript('''
        INSERT INTO categories (name, description) VALUES
        ('Розы', 'Классика'),
        ('Пионы', 'Пышные цветы'),
        ('Тюльпаны', 'Весенние'),
        ('Лилии', 'Ароматные'),
        ('Букеты', 'Готовые композиции');

        INSERT INTO flowers (name, price, photo_url, category_id, stock_quantity) VALUES
        ('Роза красная 70 см', 250.00, 'https://i.imgur.com/roses.jpg', 1, 100),
        ('Пион коралловый', 450.00, 'https://i.imgur.com/peony.jpg', 2, 50),
        ('Тюльпаны микс 51 шт', 1900.00, 'https://i.imgur.com/tulips.jpg', 3, 30),
        ('Лилия белая', 300.00, 'https://i.imgur.com/lily.jpg', 4, 70),
        ('Букет "Нежность"', 3500.00, 'https://i.imgur.com/bouquet.jpg', 5, 20);
        ''')

        await db.commit()
