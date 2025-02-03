document.addEventListener("DOMContentLoaded", () => {
    const app = document.getElementById("app");
    const volumeSelection = document.getElementById("volume-selection");
    const confirmation = document.getElementById("confirmation");
    const selectedVolume = document.getElementById("selected-volume");
    let currentAction = null;
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

    // Обработка нажатия на кнопки категорий
    document.querySelectorAll(".category-btn").forEach(button => {
        button.addEventListener("click", () => {
            currentAction = button.dataset.action;
            showVolumeSelection(currentAction);
        });
    });

    // Показать выбор объёма
    function showVolumeSelection(action) {
        const volumesDiv = document.getElementById("volumes");
        volumesDiv.innerHTML = "";
        Object.keys(prices[action]).forEach(volume => {
            const button = document.createElement("button");
            button.textContent = `${volume} м³ - ${prices[action][volume]}`;
            button.addEventListener("click", () => {
                selectedData = { action, volume, price: prices[action][volume] };
                showConfirmation();
            });
            volumesDiv.appendChild(button);
        });
        volumeSelection.style.display = "block";
        confirmation.style.display = "none";
    }

    // Показать подтверждение
    function showConfirmation() {
        selectedVolume.textContent = `Объем: ${selectedData.volume} м³\nСтоимость: ${selectedData.price}`;
        volumeSelection.style.display = "none";
        confirmation.style.display = "block";
    }

    // Подтвердить заявку
    document.getElementById("confirm-btn").addEventListener("click", () => {
        if (window.Telegram && window.Telegram.WebApp) {
            Telegram.WebApp.sendData(JSON.stringify(selectedData));
            Telegram.WebApp.close();
        } else {
            console.error("Telegram WebApp API не доступен.");
        }
    });

    // Вернуться назад
    document.getElementById("back-btn").addEventListener("click", () => {
        confirmation.style.display = "none";
        volumeSelection.style.display = "block";
    });
});