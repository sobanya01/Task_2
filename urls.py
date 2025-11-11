class Urls:
    BASE_URL = "https://stellarburgers.education-services.ru"
    CREATE_USER_ENDPOINT = f"{BASE_URL}/api/auth/register"
    AUTH_USER_ENDPOINT = f"{BASE_URL}/api/auth/login"
    LOGOUT_USER_ENDPOINT = f"{BASE_URL}/api/auth/logout"

    USER_ENDPOINT = f"{BASE_URL}/api/auth/user"

    GET_ALL_ORDERS_ENDPOINT = f"{BASE_URL}/api/orders/all"
    GET_USER_ORDERS_ENDPOINT = f"{BASE_URL}/api/orders"
    CREATE_ORDER_ENDPOINT = f"{BASE_URL}/api/orders"

    RESET_PWD_ENDPOINT = f"{BASE_URL}/api/password-reset"
    RESET_PWD_CONFIRMED_ENDPOINT = f"{BASE_URL}/api/password-reset/reset"


    GET_INGREDIENTS_ENDPOINT = f"{BASE_URL}/api/ingredients"