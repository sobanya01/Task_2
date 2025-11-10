import pytest
import allure
from clients.user_client import UserClient
from helpers import generate_random_string

@allure.epic("User Management")
@allure.feature("Change User Data")
class TestChangeUser:
    
    @allure.title("Успешное изменение данных пользователя с авторизацией")
    @allure.description("Проверяем, что авторизованный пользователь может изменить свои 'email' и 'name'.")
    @pytest.mark.parametrize("field_to_change", ["email", "name"])
    def test_change_user_data_with_auth_success(self, user, field_to_change):
        c = UserClient()
        
        with allure.step(f"Подготовка данных: генерация нового значения для поля '{field_to_change}'"):
            new_value = generate_random_string(10)
            
            if field_to_change == "email":
                payload = {"email": f"{new_value}@yandex.ru"}
                expected_email = payload["email"]
                expected_name = user["name"]
            else: # name
                payload = {"name": new_value}
                expected_email = user["email"]
                expected_name = payload["name"]

        with allure.step("Отправка запроса на изменение данных с токеном авторизации"):
            response = c.change_user(user["token"], payload)
            r_json = response.json()

        with allure.step("Проверка кода ответа и тела: 200 и 'success: true'"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            assert r_json["success"] == True, "Ожидался 'success: true'"
        
        with allure.step("Проверка, что данные пользователя обновлены корректно"):
            assert r_json["user"]["email"] == expected_email, "Email не обновился"
            assert r_json["user"]["name"] == expected_name, "Name не обновился"

    @allure.title("Изменение данных пользователя без авторизации (провал)")
    @allure.description("Проверяем, что неавторизованный пользователь не может изменить данные и получает 401.")
    def test_change_user_data_without_auth_fail(self):
        c = UserClient()
        
        with allure.step("Подготовка данных: новое имя"):
            payload = {"name": generate_random_string(10)}
        
        with allure.step("Отправка запроса на изменение данных без токена"):
            response = c.change_user(token=None, data=payload)
            r_json = response.json()
        
        with allure.step("Проверка кода ответа: 401 Unauthorized"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
            assert r_json["success"] == False, "Ожидался 'success: false'"
        
        with allure.step("Проверка сообщения об ошибке: 'You should be authorised'"):
            assert r_json["message"] == "You should be authorised", "Неверное сообщение об ошибке"

    @allure.title("Изменение email на уже существующий (провал)")
    @allure.description("Проверяем, что система возвращает ошибку 403, если новый email уже занят другим пользователем.")
    def test_change_user_email_to_existing_fail(self, user):
        c = UserClient()
        token2 = None
        
        with allure.step("Pre-condition: Создание второго пользователя (для 'занятого' email)"):
            email2 = generate_random_string(10) + "@yandex.ru"
            password2 = generate_random_string(10)
            name2 = generate_random_string(10)
            resp_user2 = c.create_user(email2, password2, name2)
            token2 = resp_user2.json().get("accessToken")
        
        with allure.step("Подготовка данных: попытка изменить email первого пользователя на email второго"):
            payload = {"email": email2}
        
        with allure.step("Отправка запроса на изменение данных"):
            response = c.change_user(user["token"], payload)
            r_json = response.json()

        with allure.step("Проверка кода ответа: 403 Forbidden"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
            assert r_json["success"] == False, "Ожидался 'success: false'"
        
        with allure.step("Проверка сообщения об ошибке: 'User with such email already exists'"):
            assert r_json["message"] == "User with such email already exists", "Неверное сообщение об ошибке"

        with allure.step("Post-condition: Удаление второго пользователя"):
            c.delete_user(token2)