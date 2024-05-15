import pytest
from conftest import register_new_courier_and_return_login_password, random_string
from utils.special_request import CourierRequests
import allure


@allure.feature('Проверка авторизации курьера, успешный запрос возвращает id')
class TestLogin:
    @allure.title('Курьер может авторизоваться с существующей учетной записью')
    def test_courier_can_login(self, create_courier_and_login):
        payload = register_new_courier_and_return_login_password()
        user = create_courier_and_login(data=payload)
        assert user['login_courier']['id']

    @pytest.mark.parametrize("remove_login", ["login"])
    @allure.title('Курьер с отсутствующим логином а не может залогиниться')
    def test_courier_cannot_login(self, remove_login, create_courier_and_login):
        payload = register_new_courier_and_return_login_password()
        user = create_courier_and_login(data=payload)
        payload.pop(remove_login)
        response = CourierRequests().post_login_courier(data=payload, status=400)
        assert response['message'] == 'Недостаточно данных для входа'

    @pytest.mark.parametrize("change_value",
                             ["login",
                              "password"]
                             )
    @allure.title('Система вернёт ошибку, если неправильно указать логин или пароль')
    def test_courier_cannot_login_due_wrong_input(self, change_value):
        payload = register_new_courier_and_return_login_password()  # create_user_payload(login='rand', password='rand', firstname='first_name')
        CourierRequests().post_create_courier(data=payload)
        payload[change_value] = random_string
        response = CourierRequests().post_login_courier(data=payload, status=404)
        assert response['message'] == 'Учетная запись не найдена'

    @allure.title('Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_courier_cant_login_for_deleted_account(self):
        payload = register_new_courier_and_return_login_password()
        CourierRequests().post_create_courier(data=payload)
        response = CourierRequests().post_login_courier(data=payload)
        courier_id = response["id"]

        response_delete = CourierRequests().delete_courier(courier_id=courier_id)
        assert response_delete['ok']
        response = CourierRequests().post_login_courier(data=payload, status=404)
        assert response["message"] == "Учетная запись не найдена"
