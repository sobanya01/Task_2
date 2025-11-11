from urls import Urls
import requests
import allure

class UserClient:
    @allure.step("Создание пользователя: email={email}, name={name}")
    def create_user(self, email, password, name):
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        
        return requests.post(Urls.CREATE_USER_ENDPOINT, data=data)
    
    @allure.step("Логин пользователя: email={email}")
    def login_user(self, email, password):
        data = {
            "email": email,
            "password": password,
        }

        return requests.post(Urls.AUTH_USER_ENDPOINT, data=data)

    @allure.step("Удаление пользователя (по токену)")
    def delete_user(self, token):
        headers = {'Authorization': token}
        return requests.delete(Urls.USER_ENDPOINT, headers=headers)

    @allure.step("Получение данных пользователя (по токену)")
    def get_user(self, token):
        headers = {'Authorization': token}
        return requests.get(Urls.USER_ENDPOINT, headers=headers)

    @allure.step("Изменение данных пользователя")
    def change_user(self, token, data):
        headers = {'Authorization': token}
        return requests.patch(Urls.USER_ENDPOINT, headers=headers, data=data)