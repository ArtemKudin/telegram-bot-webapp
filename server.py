from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import init_db, save_order, get_user_orders
import os

# Инициализация FastAPI
app = FastAPI()

# Инициализация базы данных
init_db()

# Сохранение новой заявки
@app.post("/save-order")
async def save_order_endpoint(request: Request):
    try:
        data = await request.json()
        user_id = data.get("user_id")
        service = data.get("service")
        volume = data.get("volume")
        price = data.get("price")

        if not all([user_id, service, volume, price]):
            return JSONResponse(content={"error": "Некорректные данные"}, status_code=400)

        save_order(user_id, service, volume, price)
        return JSONResponse(content={"message": "Заявка успешно сохранена"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Получение заказов пользователя
@app.post("/get-orders")
async def get_orders_endpoint(request: Request):
    try:
        data = await request.json()
        user_id = data.get("user_id")

        if not user_id:
            return JSONResponse(content={"error": "Некорректные данные"}, status_code=400)

        orders = get_user_orders(user_id)
        orders_list = [
            {"service": service, "volume": volume, "price": price}
            for service, volume, price, _ in orders
        ]
        return JSONResponse(content=orders_list)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
