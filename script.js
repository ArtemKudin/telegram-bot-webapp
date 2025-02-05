document.addEventListener("DOMContentLoaded", () => {
    const mainPage = document.getElementById("main-page");
    const volumeSelection = document.getElementById("volume-selection");
    const confirmation = document.getElementById("confirmation");
    const myOrdersPage = document.getElementById("my-orders");
    const ordersList = document.getElementById("orders-list");
    const serviceTitle = document.getElementById("service-title");
    const volumesDiv = document.getElementById("volumes");
    const selectedVolume = document.getElementById("selected-volume");
    const confirmBtn = document.getElementById("confirm-btn");
    const backToMainBtn = document.getElementById("back-to-main-btn");
    const backToVolumesBtn = document.getElementById("back-to-volumes-btn");
    const backToMainFromOrdersBtn = document.getElementById("back-to-main-from-orders-btn");
    const myOrdersBtn = document.getElementById("my-orders-btn");
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

    // Показать главную страницу
    function showMainPage() {
        mainPage.style.display = "block";
        volumeSelection.style.display = "none";
        confirmation.style.display = "none";
        myOrdersPage.style.display = "none";
    }

    // Обработка нажатия на кнопки услуг
    document.querySelectorAll(".service-btn").forEach(button => {
        button.addEventListener("click", () => {
            currentAction = button.dataset.action;
            serviceTitle.textContent = button.textContent;
            showVolumes(currentAction);
            volumeSelection.style.display = "block";
            mainPage.style.display = "none";
        });
    });

    // Показать объёмы для выбранной услуги
    function showVolumes(action) {
        volumesDiv.innerHTML = "";
        Object.keys(prices[action]).forEach(volume => {
            const button = document.createElement("button");
            button.textContent = `${volume} м³ - ${prices[action][volume]}`;
            button.onclick = () => {
                selectedData = { action, volume, price: prices[action][volume] };
                showConfirmation();
            };
            volumesDiv.appendChild(button);
        });
    }

    // Показать подтверждение
    function showConfirmation() {
        selectedVolume.textContent = `Объем: ${selectedData.volume} м³\nСтоимость: ${selectedData.price}`;
        volumeSelection.style.display = "none";
        confirmation.style.display = "block";
    }

    // Подтвердить заявку
    confirmBtn.addEventListener("click", async () => {
        if (!selectedData) {
            alert("Пожалуйста, выберите объём перед подтверждением.");
            return;
        }
        try {
            const response = await fetch("https://telegram-bot-webapp-vivoz.onrender.com/save-order", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: Telegram.WebApp.initDataUnsafe.user.id,
                    service: selectedData.action,
                    volume: selectedData.volume,
                    price: selectedData.price
                })
            });
            const result = await response.json();
            if (result.error) {
                alert(`Ошибка: ${result.error}`);
            } else {
                alert("Ваша заявка зарегистрирована!");
            }
        } catch (error) {
            console.error("Ошибка при отправке данных:", error);
            alert("Произошла ошибка при отправке данных. Попробуйте снова.");
        }
    });

    // Вернуться назад из выбора объёма
    backToMainBtn.addEventListener("click", () => {
        showMainPage();
    });

    // Вернуться назад из подтверждения
    backToVolumesBtn.addEventListener("click", () => {
        confirmation.style.display = "none";
        volumeSelection.style.display = "block";
    });

    // Показать мои заказы
    myOrdersBtn.addEventListener("click", async () => {
        try {
            const response = await fetch("https://telegram-bot-webapp-vivoz.onrender.com/get-orders", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: Telegram.WebApp.initDataUnsafe.user.id })
            });
            const orders = await response.json();
            if (orders.error) {
                ordersList.textContent = `Ошибка: ${orders.error}`;
            } else if (orders.length === 0) {
                ordersList.textContent = "У вас пока нет заказов.";
            } else {
                ordersList.textContent = orders
                    .map((order, idx) => `${idx + 1}. Услуга: ${order.service}, Объём: ${order.volume} м³, Стоимость: ${order.price}`)
                    .join("\n\n");
            }
            mainPage.style.display = "none";
            myOrdersPage.style.display = "block";
        } catch (error) {
            console.error("Ошибка при загрузке заказов:", error);
            ordersList.textContent = "Не удалось загрузить заказы.";
        }
    });

    // Вернуться назад из моих заказов
    backToMainFromOrdersBtn.addEventListener("click", () => {
        showMainPage();
    });

    // Инициализация
    showMainPage();
});