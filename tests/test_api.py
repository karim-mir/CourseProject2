import unittest
from unittest.mock import Mock, patch

import requests

from src.api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):

    @patch("requests.get")
    def test_connect_success(self, mock_get):
        # Настройка имитации успешного ответа
        mock_get.return_value = Mock(status_code=200)

        api = HeadHunterAPI()
        self.assertTrue(api.connect())

    @patch("requests.get")
    def test_connect_failure(self, mock_get):
        # Настройка имитации неуспешного ответа
        mock_get.return_value = Mock(status_code=404)

        api = HeadHunterAPI()
        self.assertFalse(api.connect())

    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        # Настройка имитации успешного ответа с данными
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "salary": {"from": 1000, "to": 2000, "currency": "RUB"},
                }
            ]
        }
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        self.assertEqual(len(vacancies["items"]), 1)
        self.assertEqual(vacancies["items"][0]["name"], "Python Developer")

    @patch("requests.get")
    def test_get_vacancies_failure(self, mock_get):
        # Настройка имитации неуспешного ответа
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError
        )  # Настройка исключения
        mock_get.return_value = mock_response

        api = HeadHunterAPI()

        # Данный вызов должен быть внутри блока с `assertRaises`
        with self.assertRaises(requests.exceptions.HTTPError):
            api.get_vacancies("Python")  # Вызов метода, который должен выдать ошибку


if __name__ == "__main__":
    unittest.main()
