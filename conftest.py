import pytest
import allure
from utils.spesial_request import CourierRequests
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


random_string = generate_random_string(10)


@allure.step('payload для пользователя')
def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    return payload


@pytest.fixture
@allure.step('payload заказа')
def create_order_payload():
    payload = {"firstName": "random_string", "lastName": "random_string",
               "address": "random_string", "metroStation": 555, "phone": "random_string", "rentTime": 10,
               "deliveryDate": "2024-02-05",
               "comment": "random_string"}
    return payload


@pytest.fixture(scope='function')
def create_courier_and_login():
    courier = {}

    def _create_courier(data):
        nonlocal courier
        courier_requests = CourierRequests()
        created_courier = courier_requests.post_create_courier(data=data)
        login_courier = courier_requests.post_login_courier(data=data)
        courier = {"created_courier": created_courier, "login_courier": login_courier}
        return courier

    yield _create_courier
    CourierRequests().delete_courier(courier_id=courier['login_courier']['id'])
