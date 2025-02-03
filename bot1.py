from aiogram import Bot, Dispatcher, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from dotenv import load_dotenv
import os
import asyncio

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

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

# Команда /myorders
@dp.message(Command("myorders"))
async def my_orders(message):
    # Проверка наличия заказов (в данном случае просто заглушка)
    orders = []  # Здесь можно добавить логику для получения реальных заказов
    if not orders:
        await message.answer(
            "У вас пока нет оплаченных заказов. Вы можете сделать заказ через мини-приложение."
        )
    else:
        # Если есть заказы, отправляем их список
        await message.answer("Ваши заказы:\n" + "\n".join(orders))

# Команда /info
@dp.message(Command("info"))
async def info_help(message):
    # Сообщение с информацией
    message_text = (
        "Уважаемый клиент,\n\n"
        "Наша компания успешно работает на рынке более 15 лет. За это время мы накопили глубокое понимание всех аспектов взаимодействия между заказчиком и исполнителем.\n\n"
        "В целях обеспечения высокого качества обслуживания мы создали круглосуточную службу поддержки, к которой вы можете обратиться в любое время суток. Также вы можете направлять нам свои замечания и предложения по улучшению нашей работы.\n\n"
        "Мы всегда открыты к диалогу и заинтересованы в долгосрочном сотрудничестве.\n\n"
        "С уважением,\nEcoService\n\n"
        "P.S. Контактные данные службы поддержки:"
    )
    # Кликабельная ссылка на контакт поддержки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="@ngKANEKI", url="https://t.me/ngKANEKI")]
    ])
    await message.answer(
        message_text,
        reply_markup=keyboard
    )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
