from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import asyncio
import json
from database import init_db, save_order, get_user_orders

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация базы данных
init_db()

# FastAPI приложение
app = FastAPI()

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message):
    await message.answer("Добро пожаловать! Используйте меню для взаимодействия.")

# Команда /order
@dp.message(Command("order"))
async def order_pickup(message):
    # Кнопка для запуска мини-приложения
    web_app_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть мини-приложение", web_app=WebAppInfo(url="https://artemkudin.github.io/telegram-bot-webapp/"))]
    ])
    await message.answer(
        "Вы можете заказать вывоз мусора через наше мини-приложение:",
        reply_markup=web_app_keyboard
    )

# Обработка данных из мини-приложения
@dp.message(F.web_app_data)
async def handle_web_app_data(message):
    try:
        # Преобразуем JSON-строку в словарь
        data_dict = json.loads(message.web_app_data.data)
        user_id = message.from_user.id
        service = data_dict.get("action")
        volume = data_dict.get("volume")
        price = data_dict.get("price")

        # Проверяем, что все данные получены
        if not all([service, volume, price]):
            await message.answer("Ошибка: Некорректные данные заявки.")
            return

        # Сохраняем заявку в базу данных
        save_order(user_id, service, volume, price)

        # Отправляем подтверждение пользователю
        await message.answer("Ваша заявка зарегистрирована. Для оплаты перейдите по ссылке:")
    except Exception as e:
        print(f"Ошибка при обработке данных: {str(e)}")
        await message.answer("Произошла ошибка при обработке заявки. Попробуйте снова.")

# Запрос для получения заказов
@app.post("/get-orders")
async def get_orders(request: Request):
    try:
        data = await request.json()
        user_id = data.get("user_id")
        orders = get_user_orders(user_id)
        return JSONResponse(content=orders)
    except Exception as e:
        print(f"Ошибка при получении заказов: {str(e)}")
        return JSONResponse(content=[], status_code=500)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
