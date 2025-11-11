import pytest
import allure
from clients.order_client import OrderClient
from data import Message


@allure.epic("Orders")
@allure.feature("Get User's Orders")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя (успех)")
    @allure.description("Сценарий: авторизованный пользователь. Ожидаем 200 и список заказов.")
    def test_get_user_orders_with_auth_success(self, user, ingredients_list):
        c = OrderClient()

        with allure.step("Pre-condition: Создание заказа, чтобы список не был пустым"):
            payload = [ingredients_list[0], ingredients_list[1]]
            create_response = c.create_order(payload, user["token"])
            assert create_response.status_code == 200, "Не удалось создать заказ для теста"

        with allure.step("Отправка запроса на получение заказов пользователя"):
            response = c.get_user_orders(user["token"])
            r_json = response.json()

        with allure.step("Проверка кода ответа и тела: 200 и 'success: true'"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            assert r_json["success"] == True, "Ожидался 'success: true'"

        with allure.step("Проверка, что получен список 'orders' и он не пуст"):
            assert "orders" in r_json, "Ответ не содержит 'orders'"
            assert isinstance(r_json["orders"], list), "'orders' должен быть списком"
            assert len(r_json["orders"]) > 0, "Список заказов не должен быть пустым"

    @allure.title("Получение заказов неавторизованного пользователя (провал)")
    @allure.description("Сценарий: неавторизованный пользователь. Ожидаем 401.")
    def test_get_user_orders_without_auth_fail(self):
        c = OrderClient()

        with allure.step("Отправка запроса на получение заказов БЕЗ авторизации"):
            response = c.get_user_orders(token=None)
            r_json = response.json()

        with allure.step("Проверка кода ответа: 401 Unauthorized"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
            assert r_json["success"] == False, "Ожидался 'success: false'"

        with allure.step("Проверка сообщения об ошибке: 'You should be authorised'"):
            assert r_json["message"] == Message.YOU_SHOULD_BE_AUTHORIZED, "Неверное сообщение об ошибке"
