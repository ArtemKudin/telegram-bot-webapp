document.addEventListener("DOMContentLoaded", () => {
    // Проверяем, что мини-приложение запущено в Telegram
    if (!window.Telegram || !window.Telegram.WebApp) {
        alert("Это мини-приложение должно запускаться только через Telegram!");
        return;
    }

    const serviceInfo = document.getElementById("service-info");
    const serviceTitle = document.getElementById("service-title");
    const volumesDiv = document.getElementById("volumes");
    const confirmBtn = document.getElementById("confirm-btn");
    let selectedData = null;

    // Цены для каждой категории
    const prices = {
        service_waste: {
            "0.8": "900 рублей",
            "1.1": "1000 рублей",
            "8": "10 000 рублей",
            "20": "25 000 рублей",
            "27": "30 000 рублей"
        },
        service_sale: {
            "0.8": "15 000 рублей + доставка",
            "1.1": "20 000 рублей + доставка",
            "8": "60 000 рублей + доставка",
            "20": "640 000 рублей + доставка",
            "27": "750 000 рублей + доставка"
        },
        service_rent: {
            "0.8": "1500 рублей",
            "1.1": "2000 рублей",
            "8": "15 000 рублей",
            "20": "20 000 рублей",
            "27": "25 000 рублей"
        }
    };

    // Обработка нажатия на кнопки услуг
    document.querySelectorAll(".service-btn").forEach(button => {
        button.addEventListener("click", () => {
            const action = button.dataset.action;
            serviceTitle.textContent = button.textContent;
            showVolumes(action);
            serviceInfo.style.display = "block";
            confirmBtn.disabled = true; // Отключаем кнопку "Подтвердить" до выбора объёма
        });
    });

    // Показать объёмы для выбранной услуги
    function showVolumes(action) {
        volumesDiv.innerHTML = ""; // Очищаем предыдущие кнопки
        Object.keys(prices[action]).forEach(volume => {
            const button = document.createElement("button");
            button.textContent = `${volume} м³ - ${prices[action][volume]}`;
            button.onclick = () => {
                selectedData = { action, volume, price: prices[action][volume] };
                confirmBtn.disabled = false; // Включаем кнопку "Подтвердить"
                alert(`Выбрано: ${volume} м³ за ${prices[action][volume]}`);
            };
            volumesDiv.appendChild(button);
        });
    }

    // Подтвердить заявку
    confirmBtn.addEventListener("click", () => {
        if (selectedData) {
            Telegram.WebApp.sendData(JSON.stringify(selectedData));
            Telegram.WebApp.close();
        } else {
            alert("Пожалуйста, выберите объём перед подтверждением.");
        }
    });
});