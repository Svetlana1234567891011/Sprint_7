import pytest
import allure
from utils.special_request import OrderRequests


@allure.feature('Создание и выгрузка заказов')
class TestOrder:
    @allure.title('Можно указать один из цветов — BLACK или GREY, ответ содержит "track"')
    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],])
    def test_create_order_successful(self, color, create_order_payload):
        payload = create_order_payload
        payload["color"] = color
        response = OrderRequests().post_create_order(data=payload)
        assert "track" in response

    @allure.title('Можно не указывать цвет, ответ содержит "track"')
    def test_order_no_color(self, create_order_payload):
        payload = create_order_payload
        response = OrderRequests().post_create_order(data=payload)
        assert "track" in response

    @allure.title('Тело ответа возвращается список заказов')
    def test_get_order_list(self):
        response = OrderRequests().list_of_orders()
        assert "orders" in response
