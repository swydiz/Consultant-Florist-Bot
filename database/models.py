#переводчик между Python-кодом и таблицами в PostgreSQL
# models.py
from sqlalchemy import (
    Column, Integer, BigInteger, String, Text, Numeric, ForeignKey, DateTime, func
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)           # telegram_id
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    allergy = Column(Text)
    role = Column(String(20), default="user")

    # Связи (пока не используем, но пригодятся позже)
    orders = relationship("Order", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    flowers = relationship("Flower", back_populates="category")


class Flower(Base):
    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    photo_url = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    stock_quantity = Column(Integer, default=999)

    category = relationship("Category", back_populates="flowers")
    orders = relationship("Order", back_populates="flower")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id"))
    quantity = Column(Integer, default=1)
    price_at_order = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="pending")  # pending = в корзине

    user = relationship("User", back_populates="orders")
    flower = relationship("Flower", back_populates="orders")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    chat_id = Column(BigInteger)
    content = Column(Text, nullable=False)
    role = Column(String(10), nullable=False)  # 'user' или 'bot'
    created_at = Column(DateTime, server_default=func.now())