// Инициализация Telegram Web App
const tg = window.Telegram.WebApp;

// Отправка данных в бот при нажатии на кнопки
document.getElementById('waste').addEventListener('click', () => {
    tg.sendData(JSON.stringify({ action: 'service_waste' }));
    tg.close();
});

document.getElementById('sale').addEventListener('click', () => {
    tg.sendData(JSON.stringify({ action: 'service_sale' }));
    tg.close();
});

document.getElementById('rent').addEventListener('click', () => {
    tg.sendData(JSON.stringify({ action: 'service_rent' }));
    tg.close();
});