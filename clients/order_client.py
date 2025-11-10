import requests
import allure
from urls import Urls

class OrderClient:
    @allure.step("Получение списка всех ингредиентов")
    def get_ingredients(self):
        return requests.get(Urls.GET_INGREDIENTS_ENDPOINT)

    @allure.step("Создание заказа")
    def create_order(self, ingredients, token=None):
        data = {"ingredients": ingredients}
        headers = {'Authorization': token}
        
        return requests.post(Urls.CREATE_ORDER_ENDPOINT, json=data, headers=headers)

    @allure.step("Получение заказов пользователя")
    def get_user_orders(self, token=None):
        headers = {'Authorization': token}
        
        return requests.get(Urls.GET_USER_ORDERS_ENDPOINT, headers=headers)