import pytest
import allure
from clients.order_client import OrderClient

@allure.epic("Orders")
@allure.feature("Create Order")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами (успех)")
    @allure.description("Сценарий: с авторизацией, с ингредиентами. Ожидаем 200.")
    def test_create_order_with_auth_and_ingredients_success(self, user, ingredients_list):
        c = OrderClient()
        
        with allure.step("Подготовка данных: выбор валидных ингредиентов"):
            payload = [ingredients_list[0], ingredients_list[1]]
        
        with allure.step("Отправка запроса на создание заказа с авторизацией"):
            response = c.create_order(payload, user["token"])
            r_json = response.json()

        with allure.step("Проверка кода ответа и тела: 200 и 'success: true'"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            assert r_json["success"] == True, "Ожидался 'success: true'"
        
        with allure.step("Проверка наличия и не-пустоты номера заказа"):
            assert "order" in r_json, "Ответ не содержит 'order'"
            assert "number" in r_json["order"], "Заказ не содержит 'number'"
            assert r_json["order"]["number"] is not None, "Номер заказа не должен быть null"

    @allure.title("Создание заказа без авторизации (провал)")
    @allure.description("Сценарий: без авторизации, с ингредиентами. Ожидаем 401.")
    def test_create_order_without_auth_fail(self, ingredients_list):
        c = OrderClient()
        
        with allure.step("Подготовка данных: выбор валидных ингредиентов"):
            payload = [ingredients_list[0], ingredients_list[1]]

        with allure.step("Отправка запроса на создание заказа БЕЗ авторизации"):
            response = c.create_order(payload, token=None)
            r_json = response.json()

        with allure.step("Проверка кода ответа: 401 Unauthorized"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
            assert r_json["success"] == False, "Ожидался 'success: false'"

        with allure.step("Проверка сообщения об ошибке: 'You should be authorised'"):
            assert r_json["message"] == "You should be authorised", "Неверное сообщение об ошибке"


    @allure.title("Создание заказа с авторизацией, но без ингредиентов (провал)")
    @allure.description("Сценарий: с авторизацией, без ингредиентов. Ожидаем 400.")
    def test_create_order_with_auth_no_ingredients_fail(self, user):
        c = OrderClient()
        
        with allure.step("Подготовка данных: пустой список ингредиентов"):
            payload = []
        
        with allure.step("Отправка запроса на создание заказа БЕЗ ингредиентов"):
            response = c.create_order(payload, user["token"])
            r_json = response.json()

        with allure.step("Проверка кода ответа: 400 Bad Request"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
            assert r_json["success"] == False, "Ожидался 'success: false'"
        
        with allure.step("Проверка сообщения об ошибке: 'Ingredient ids must be provided'"):
            assert r_json["message"] == "Ingredient ids must be provided", "Неверное сообщение об ошибке"

    @allure.title("Создание заказа с неверным хешем ингредиентов (провал)")
    @allure.description("Сценарий: с авторизацией, с неверным хешем ингредиентов. Ожидаем 500.")
    def test_create_order_with_auth_invalid_hash_fail(self, user):
        c = OrderClient()
        
        with allure.step("Подготовка данных: невалидные хеши ингредиентов"):
            payload = ["invalid_hash_12345", "another_fake_hash"]
        
        with allure.step("Отправка запроса на создание заказа с невалидным хешем"):
            response = c.create_order(payload, user["token"])

        with allure.step("Проверка кода ответа: 500 Internal Server Error"):
            assert response.status_code == 500, f"Ожидался код 500, получен {response.status_code}"