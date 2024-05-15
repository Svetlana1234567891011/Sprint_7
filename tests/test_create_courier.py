import pytest
import allure
from conftest import random_string
from conftest import register_new_courier_and_return_login_password
from utils.special_request import CourierRequests


@allure.feature('Создание курьера')
class TestCreateCourier:
    @allure.title('Можно создать курьера со случайным логином')
    def test_can_create_courier(self):
        payload = register_new_courier_and_return_login_password()
        response = CourierRequests().post_create_courier(data=payload)
        assert response['ok']

    @allure.title('Нельзя создать двух курьеров с одинаковыми логинами')
    def test_cant_create_courier_dupes(self):
        payload = register_new_courier_and_return_login_password()
        CourierRequests().post_create_courier(data=payload)  # отправляем данные

        response_dupe = CourierRequests().post_create_courier(data=payload, status=409)  # отправляем данные повторно
        assert response_dupe["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize('login_v, password_v, firstname_v',
                             [
                                 (None, random_string, random_string),
                                 (None, random_string, None),
                                 (random_string, None, None),
                                 (None, None, random_string),


                             ])
    @allure.title('Для создания курьера необходимо задать все обязательные поля (логин, пароль)')
    def test_all_the_fields_are_required(self, login_v, password_v, firstname_v):
        payload = {
            "login": login_v,
            "password": password_v,
            "firstName": firstname_v
        }

        response = CourierRequests().post_create_courier(data=payload, status=400)
        assert response["message"] == "Недостаточно данных для создания учетной записи"
