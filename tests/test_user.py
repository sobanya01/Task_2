import pytest
import allure
from clients.user_client import UserClient
from helpers import generate_random_string
from data import *


@allure.epic("User Management")
@allure.feature("Create User")
class TestUser:
    @allure.title("Создание уникального пользователя (успех)")
    @allure.description("Проверяем, что система успешно создает нового пользователя с уникальными данными.")
    def test_create_unique_user(self):
        c = UserClient()

        with allure.step("Подготовка данных: генерация email, password, name"):
            email = generate_random_string(10) + "@yandex.ru"
            password = generate_random_string(10)
            name = generate_random_string(10)

        with allure.step("Отправка запроса на создание уникального пользователя"):
            response = c.create_user(email=email, password=password, name=name)
            r_json = response.json()

        with allure.step("Проверка кода ответа и тела: 200 и 'success: true'"):
            assert response.status_code == 200
            assert r_json["success"] == True

        with allure.step("Проверка наличия токена доступа"):
            assert "accessToken" in r_json
            assert r_json["accessToken"] is not ""

        with allure.step("Post-condition: Удаление тестового пользователя"):
            c.delete_user(r_json["accessToken"])

    @allure.title("Создание пользователя, который уже зарегистрирован (провал)")
    @allure.description("Проверяем, что система возвращает ошибку 403 при попытке повторной регистрации.")
    def test_create_existing_user(self):
        c = UserClient()

        with allure.step("Подготовка данных: генерация и первая регистрация пользователя"):
            email = generate_random_string(10) + "@yandex.ru"
            password = generate_random_string(10)
            name = generate_random_string(10)
            response1 = c.create_user(email=email, password=password, name=name)
            token1 = response1.json().get("accessToken")

        with allure.step("Отправка второго (дублирующего) запроса на создание пользователя"):
            response2 = c.create_user(email=email, password=password, name=name)
            r_json = response2.json()

        with allure.step("Проверка кода ответа и тела: 403 Forbidden"):
            assert response2.status_code == 403
            assert r_json["success"] == False

        with allure.step("Проверка сообщения об ошибке: 'User already exists'"):
            assert r_json["message"] == Message.USER_ALREADY_EXISTS

        if token1:
            with allure.step("Post-condition: Удаление тестового пользователя"):
                c.delete_user(token1)

    @allure.title("Создание пользователя без одного из обязательных полей (провал)")
    @allure.description("Параметризованный тест: проверяем 403, если отсутствует email, password или name.")
    @pytest.mark.parametrize("case_id, email, password, name", CREATE_USER_DATA_MISSING_FIELDS)
    def test_create_user_with_invalid_fields(self, case_id, email, password, name):
        c = UserClient()

        with allure.step(f"Подготовка данных: Проверка сценария '{case_id}'"):
            pass

        with allure.step(f"Отправка запроса на создание пользователя"):
            response = c.create_user(email=email, password=password, name=name)
            r_json = response.json()

        with allure.step("Проверка кода ответа и тела: 403 Forbidden"):
            assert response.status_code == 403
            assert r_json["success"] == False

        with allure.step("Проверка сообщения об ошибке: 'Email, password and name are required fields'"):
            assert r_json["message"] == Message.REQUIRED_FIELDS_MISSED
