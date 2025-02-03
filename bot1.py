from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils import executor
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    # Создание кнопок меню
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("📦 Заказать вывоз", callback_data="order_pickup"),
        InlineKeyboardButton("📋 Мои заказы", callback_data="my_orders"),
        InlineKeyboardButton("ℹ️ Информация и помощь", callback_data="info_help")
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)

# Обработчик для кнопки "Заказать вывоз"
@dp.callback_query_handler(lambda c: c.data == "order_pickup")
async def order_pickup(callback_query: types.CallbackQuery):
    # Кнопка для запуска мини-приложения
    web_app_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть мини-приложение", web_app=WebAppInfo(url="https://artemkudin.github.io/telegram-bot-webapp/"))]
    ])
    await bot.send_message(
        callback_query.from_user.id,
        "Вы можете заказать вывоз мусора через наше мини-приложение:",
        reply_markup=web_app_keyboard
    )

# Обработчик для кнопки "Мои заказы"
@dp.callback_query_handler(lambda c: c.data == "my_orders")
async def my_orders(callback_query: types.CallbackQuery):
    # Проверка наличия заказов (в данном случае просто заглушка)
    orders = []  # Здесь можно добавить логику для получения реальных заказов
    if not orders:
        await bot.send_message(
            callback_query.from_user.id,
            "У вас пока нет оплаченных заказов. Вы можете сделать заказ через мини-приложение."
        )
    else:
        # Если есть заказы, отправляем их список
        await bot.send_message(callback_query.from_user.id, "Ваши заказы:\n" + "\n".join(orders))

# Обработчик для кнопки "Информация и помощь"
@dp.callback_query_handler(lambda c: c.data == "info_help")
async def info_help(callback_query: types.CallbackQuery):
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
    await bot.send_message(
        callback_query.from_user.id,
        message_text,
        reply_markup=keyboard
    )

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
