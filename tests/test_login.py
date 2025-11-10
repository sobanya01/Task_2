import pytest
import allure
from clients.user_client import UserClient
from helpers import generate_random_string

@allure.epic("User Management")
@allure.feature("Login User")
class TestLogin:
    @allure.title("Логин под существующим пользователем (успех)")
    @allure.description("Проверяем, что созданный пользователь может успешно войти в систему.")
    def test_login_existing_user(self, user):
        c = UserClient()

        with allure.step("Отправка запроса на логин существующего пользователя"):
            response = c.login_user(email=user["email"], password=user["password"])
            r_json = response.json()

        with allure.step("Проверка кода ответа и тела: 200 и 'success: true'"):
            assert response.status_code == 200
            assert r_json["success"] == True

        with allure.step("Проверка наличия токена доступа"):
            assert "accessToken" in r_json
            assert r_json["accessToken"] is not ""

    @allure.title("Логин с неверным логином и паролем (провал)")
    @allure.description("Проверяем, что система возвращает 401 Unauthorized при неверных учетных данных.")
    def test_login_non_existing_user(self):
        with allure.step("Подготовка данных: генерация несуществующего пользователя"):
            email = generate_random_string(10) + "@yandex.ru"
            password = generate_random_string(10)

        c = UserClient()
        
        with allure.step("Отправка запроса на логин с неверными данными"):
            response = c.login_user(email=email, password=password)
        
        with allure.step("Проверка кода ответа: 401 Unauthorized"):
            assert response.status_code == 401
        
        with allure.step("Проверка сообщения об ошибке"):
            r_json = response.json()
            assert r_json["success"] == False
            assert r_json["message"] == "email or password are incorrect"