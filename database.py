import sqlite3
from datetime import datetime

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payment_link = f"https://example.com/pay?order_id={datetime.now().timestamp()}"  # Генерация ссылки для оплаты
    cursor.execute("""
        INSERT INTO orders (user_id, service, volume, price, timestamp, payment_link)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, service, volume, price, timestamp, payment_link))
    conn.commit()
    conn.close()

# Получение заявок пользователя
def get_user_orders(user_id):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT service, volume, price, payment_link FROM orders WHERE user_id = ?", (user_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders
