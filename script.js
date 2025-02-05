document.addEventListener("DOMContentLoaded", () => {
    const mainPage = document.getElementById("menu");
    const servicesPage = document.getElementById("services");
    const confirmPage = document.getElementById("confirm-order");
    const ordersPage = document.getElementById("orders");
    const ordersList = document.getElementById("orders-list");
    const orderDetails = document.getElementById("order-details");

    let selectedService = null;
    let selectedVolume = null;

    // Цены для каждой категории
    const prices = {
        "Вывоз мусора": {
            "0.8": "900 рублей",
            "1.1": "1000 рублей",
            "8": "10 000 рублей",
            "20": "25 000 рублей",
            "27": "30 000 рублей"
        },
        "Продажа контейнеров": {
            "0.8": "15 000 рублей + доставка",
            "1.1": "20 000 рублей + доставка",
            "8": "60 000 рублей + доставка",
            "20": "640 000 рублей + доставка",
            "27": "750 000 рублей + доставка"
        },
        "Аренда контейнеров": {
            "0.8": "1500 рублей",
            "1.1": "2000 рублей",
            "8": "15 000 рублей",
            "20": "20 000 рублей",
            "27": "25 000 рублей"
        }
    };

    // Показать страницу выбора услуг
    function showServices() {
        mainPage.classList.add("hidden");
        servicesPage.classList.remove("hidden");
    }

    // Выбор услуги
    function selectService(service) {
        selectedService = service;
        servicesPage.classList.add("hidden");
        confirmPage.classList.remove("hidden");

        // Очистка предыдущих данных
        orderDetails.innerHTML = "";
        Object.keys(prices[service]).forEach(volume => {
            const button = document.createElement("button");
            button.textContent = `${volume} м³ - ${prices[service][volume]}`;
            button.onclick = () => {
                selectedVolume = volume;
                orderDetails.textContent = `Услуга: ${service}, Объем: ${volume} м³, Стоимость: ${prices[service][volume]}`;
            };
            orderDetails.appendChild(button);
        });
    }

    // Подтвердить заказ
    async function confirmOrder() {
        if (!selectedService || !selectedVolume) {
            alert("Пожалуйста, выберите услугу и объем.");
            return;
        }

        try {
            const response = await fetch("https://your-render-url/save-order", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_id: Telegram.WebApp.initDataUnsafe.user.id,
                    service: selectedService,
                    volume: selectedVolume,
                    price: prices[selectedService][selectedVolume]
                })
            });

            const result = await response.json();
            if (result.error) {
                alert(`Ошибка: ${result.error}`);
            } else {
                alert("Ваш заказ успешно зарегистрирован!");
                goBack();
            }
        } catch (error) {
            console.error("Ошибка при отправке данных:", error);
            alert("Произошла ошибка при отправке данных. Попробуйте снова.");
        }
    }

    // Показать мои заказы
    async function showOrders() {
        try {
            const response = await fetch("https://your-render-url/get-orders", {
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
                ordersList.innerHTML = orders
                    .map((order, idx) => `<li>${idx + 1}. Услуга: ${order.service}, Объем: ${order.volume} м³, Стоимость: ${order.price}</li>`)
                    .join("");
            }

            mainPage.classList.add("hidden");
            ordersPage.classList.remove("hidden");
        } catch (error) {
            console.error("Ошибка при загрузке заказов:", error);
            ordersList.textContent = "Не удалось загрузить заказы.";
        }
    }

    // Вернуться назад
    function goBack() {
        confirmPage.classList.add("hidden");
        ordersPage.classList.add("hidden");
        servicesPage.classList.add("hidden");
        mainPage.classList.remove("hidden");
    }

    // Привязка событий
    document.querySelector("#menu button:first-child").onclick = showServices;
    document.querySelector("#menu button:last-child").onclick = showOrders;
});