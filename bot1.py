from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
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

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message):
    # Кнопка для запуска мини-приложения
    web_app_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть мини-приложение", web_app=WebAppInfo(url="https://artemkudin.github.io/telegram-bot-webapp/"))]
    ])
    await message.answer(
        "Добро пожаловать! Используйте меню для взаимодействия.\n\n"
        "Вы можете заказать вывоз мусора через наше мини-приложение:",
        reply_markup=web_app_keyboard
    )

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

# Команда /myorders
@dp.message(Command("myorders"))
async def my_orders(message):
    user_id = message.from_user.id
    orders = get_user_orders(user_id)
    if not orders:
        await message.answer("У вас пока нет зарегистрированных заявок.")
        return
    response = "Ваши заявки:\n\n"
    for idx, (service, volume, price, payment_link) in enumerate(orders, start=1):
        response += f"{idx}. Услуга: {service}, Объём: {volume} м³, Стоимость: {price}\n"
        response += f"Для оплаты перейдите по ссылке: {payment_link}\n\n"
    await message.answer(response)

# Обработка данных из мини-приложения
@dp.message(F.web_app_data)
async def handle_web_app_data(message):
    try:
        # Преобразуем JSON-строку в словарь
        data_dict = json.loads(message.web_app_data.data)
        user_id = message.from_user.id
        logging.info(f"Received data: {data_dict}")
        # Если запрос на получение заказов
        if data_dict.get("action") == "get_orders":
            orders = get_user_orders(user_id)
            if not orders:
                await message.answer("У вас пока нет заказов.")
                return
            # Отправляем заказы в формате JSON
            orders_list = [
                {"service": service, "volume": volume, "price": price}
                for service, volume, price, _ in orders
            ]
            await message.answer(json.dumps(orders_list))
            return
        # Если запрос на сохранение новой заявки
        service = data_dict.get("action")
        volume = data_dict.get("volume")
        price = data_dict.get("price")
        logging.info(f"Service: {service}, Volume: {volume}, Price: {price}")
        # Проверяем, что все данные получены
        if not all([service, volume, price]):
            await message.answer("Ошибка: Некорректные данные заявки.")
            return
        # Сохраняем заявку в базу данных
        save_order(user_id, service, volume, price)
        # Отправляем подтверждение пользователю
        await message.answer("Ваша заявка зарегистрирована. Для оплаты перейдите по ссылке:")
    except Exception as e:
        logging.error(f"Ошибка при обработке данных: {str(e)}")
        await message.answer("Произошла ошибка при обработке заявки. Попробуйте снова.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
