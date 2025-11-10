import pytest
from helpers import generate_random_string
from clients.user_client import UserClient
from clients.order_client import OrderClient

@pytest.fixture
def user():
    c = UserClient()

    email=generate_random_string(10) + "@yandex.ru"
    password=generate_random_string(10)
    name=generate_random_string(10)

    response = c.create_user(email=email, password=password, name=name)

    r_json = response.json()

    data = {
        "email": email,
        "password": password,
        "name": name,
        "token": r_json["accessToken"]
    }

    yield data

    c.delete_user(data["token"])


@pytest.fixture(scope="session")
def ingredients_list():
    c = OrderClient()
    response = c.get_ingredients()
    assert response.status_code == 200, "Не удалось получить список ингредиентов"
    data = response.json()
    assert data["success"] == True
    
    hashes = [ing['_id'] for ing in data['data']]
    return hashes