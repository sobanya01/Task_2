
EMAIL = "test_email@yandex.ru"
NAME = "test_name"
PASSWORD = "test_password"
CREATE_USER_DATA_MISSING_FIELDS = [
    ("Отсуствует email", "", PASSWORD, NAME),
    ("Отсуствует password", EMAIL, "", NAME),
    ("Отсуствует name", EMAIL, PASSWORD, ""),
]