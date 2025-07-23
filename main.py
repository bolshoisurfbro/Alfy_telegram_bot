import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Загружаем переменные из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверяем, есть ли токен
if not BOT_TOKEN:
    print("Пожалуйста, добавьте переменную BOT_TOKEN в .env файл")
    exit(1)

# Создаем экземпляр бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я готов работать 🚀")

# Обработчик любых текстовых сообщений
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer("Вы написали: " + message.text)

# Точка входа
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
