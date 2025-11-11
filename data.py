EMAIL = "test_email@yandex.ru"
NAME = "test_name"
PASSWORD = "test_password"
CREATE_USER_DATA_MISSING_FIELDS = [
    ("Отсуствует email", "", PASSWORD, NAME),
    ("Отсуствует password", EMAIL, "", NAME),
    ("Отсуствует name", EMAIL, PASSWORD, ""),
]


class Message:
    YOU_SHOULD_BE_AUTHORIZED = "You should be authorised"
    USER_WITH_EMAIL_ALREADY_EXISTS = "User with such email already exists"
    INGREDIENT_IDS_MUST_BE_PROVIDED = "Ingredient ids must be provided"
    INCORRECT_EMAIL_PASSWORD = "email or password are incorrect"
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS_MISSED = "Email, password and name are required fields"
