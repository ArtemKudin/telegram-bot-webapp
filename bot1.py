from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
import asyncio
import json
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")  # Загружаем токен из .env

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Кнопка для открытия мини-приложения
web_app_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Открыть мини-приложение", web_app=WebAppInfo(url="https://artemkudin.github.io/telegram-bot-webapp/"))]
])

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Добро пожаловать! Нажмите на кнопку ниже, чтобы открыть мини-приложение.",
        reply_markup=web_app_keyboard
    )

# Обработка данных из мини-приложения
@dp.message()
async def handle_webapp_data(message: types.Message):
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        action = data.get('action')
        volume = data.get('volume')
        price = data.get('price')

        service_name = {
            "service_waste": "вывоза мусора 🚛",
            "service_sale": "покупки контейнера 💰",
            "service_rent": "аренды контейнера 🏠"
        }.get(action, "неизвестной услуги")

        await message.answer(
            f"✅ Ваша заявка на {service_name} зарегистрирована!\n"
            f"Объем: {volume} м³\n"
            f"Стоимость: {price}\n\n"
            f"Для оплаты и уточнения деталей обратитесь к менеджеру: @ngKANEKI 📞\n"
            f"Спасибо, что выбрали нас! 🌟"
        )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
