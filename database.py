import psycopg2
from datetime import datetime
import os

# Настройки подключения к PostgreSQL через переменные окружения
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432")
}

# Инициализация базы данных
def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            service TEXT,
            volume TEXT,
            price TEXT,
            timestamp TEXT,
            payment_link TEXT
        )
    """)
    conn.commit()
    conn.close()

# Сохранение новой заявки
def save_order(user_id, service, volume, price):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payment_link = f"https://example.com/pay?order_id={datetime.now().timestamp()}"  # Генерация ссылки для оплаты
    cursor.execute("""
        INSERT INTO orders (user_id, service, volume, price, timestamp, payment_link)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, service, volume, price, timestamp, payment_link))
    conn.commit()
    conn.close()

# Получение заявок пользователя
def get_user_orders(user_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT service, volume, price, payment_link FROM orders WHERE user_id = %s", (user_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders
