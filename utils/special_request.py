import json
import requests
import allure


class MainRequests:
    host = 'https://qa-scooter.praktikum-services.ru'

    def post_request_transform_and_check(self, url, data, status):  # проверяем код ответа
        response = requests.post(url=url, data=data)  # кладем код ответа в переменную response
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:  # Функция exec_post_request_and_check проверяет
            return response.json()  # статус ответа и, если тип содержимого ответа - JSON, возвращает его в формате словаря, иначе возвращает текст ответа.
        else:
            return response.text

    def delete_request_transform_and_check(self, url, data, status):
        response = requests.delete(url=url, data=data)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def get_request_transform_and_check(self, url, status):
        response = requests.get(url=url)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def put_request_transform_and_check(self, url, data, status):
        response = requests.put(url=url, data=data)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text


class CourierRequests(MainRequests):
    courier_create = '/api/v1/courier'
    courier_login = '/api/v1/courier/login'

    @allure.step('Создаем курьера, отправив запрос POST. Ожидаем статус ответа {status}')
    def post_create_courier(self, data=None, status=201):
        url = f"{self.host}{self.courier_create}"
        return self.post_request_transform_and_check(url, data=data, status=status)

    @allure.step('Логиним курьера, отправив запрос POST. Ожидаем статус респонса {status}')
    def post_login_courier(self, data=None, status=200):
        url = f"{self.host}{self.courier_login}"
        return self.post_request_transform_and_check(url, data=data, status=status)

    @allure.step('Удаляем курьера, отправив запрос DELETE. Ожидаем статус респонса {status}')
    def delete_courier(self, courier_id=None, status=200):
        url = f"{self.host}{self.courier_create}/{courier_id}"
        delete_payload = {"id": courier_id}
        return self.delete_request_transform_and_check(url, data=delete_payload, status=status)


class OrderRequests(MainRequests):
    order_point = '/api/v1/orders'

    @allure.step('Создаем заказ, отправив запрос POST. Ожидаем статус респонса {status}')
    def post_create_order(self, data=None, status=201):
        url = f"{self.host}{self.order_point}"
        return self.post_request_transform_and_check(url, data=json.dumps(data), status=status)

    @allure.step('Отправляем get, получаем список заказов')
    def list_of_orders(self, status=200):
        url = f"{self.host}{self.order_point}"
        return self.get_request_transform_and_check(url, status=status)
