import json
import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.files import JSONSaver  # Замените 'your_module' на имя вашего модуля


class TestJSONSaver(unittest.TestCase):

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_load_vacancies_file_not_exist(self, mock_file, mock_exists):
        mock_exists.return_value = False
        saver = JSONSaver()
        self.assertEqual(saver.vacancies, [])

    @patch("os.path.exists")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='[{"title": "Vacancy 1", "link": "http://example.com/1"}]',
    )
    def test_load_vacancies_file_exists(self, mock_file, mock_exists):
        mock_exists.return_value = True
        saver = JSONSaver()
        self.assertEqual(len(saver.vacancies), 1)
        self.assertEqual(saver.vacancies[0]["title"], "Vacancy 1")

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="")  # Пустой файл
    def test_load_vacancies_empty_file(self, mock_file, mock_exists):
        mock_exists.return_value = True
        saver = JSONSaver()
        self.assertEqual(saver.vacancies, [])

    @patch("os.path.exists")
    @patch(
        "builtins.open", new_callable=mock_open, read_data="not a json"
    )  # Некорректный JSON
    def test_load_vacancies_invalid_json(self, mock_file, mock_exists):
        mock_exists.return_value = True
        saver = JSONSaver()
        self.assertEqual(saver.vacancies, [])

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_save_vacancies(self, mock_makedirs, mock_file):
        saver = JSONSaver()
        saver.vacancies = [{"title": "Vacancy 1", "link": "http://example.com/1"}]
        saver.save_vacancies()

        # Получаем ожидаемую строку JSON
        expected_json = json.dumps(saver.vacancies, ensure_ascii=False, indent=4)

        # Объединяем все вызовы write в одну строку
        all_calls = "".join(call[0][0] for call in mock_file().write.call_args_list)

        # Проверяем, что полный вызов write соответствует ожидаемому JSON
        self.assertEqual(all_calls, expected_json)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_add_vacancy(self, mock_makedirs, mock_file):
        saver = JSONSaver()
        saver.vacancies = []
        vacancy = {"title": "Vacancy 1", "link": "http://example.com/1"}
        saver.add_vacancy(vacancy)
        self.assertEqual(len(saver.vacancies), 1)
        self.assertEqual(saver.vacancies[0], vacancy)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    def test_delete_vacancy(self, mock_makedirs, mock_file):
        saver = JSONSaver()
        saver.vacancies = [
            {"title": "Vacancy 1", "link": "http://example.com/1"},
            {"title": "Vacancy 2", "link": "http://example.com/2"},
        ]
        vacancy_to_delete = MagicMock()
        vacancy_to_delete.link = "http://example.com/1"
        saver.delete_vacancy(vacancy_to_delete)
        self.assertEqual(len(saver.vacancies), 1)
        self.assertEqual(saver.vacancies[0]["link"], "http://example.com/2")

    def test_get_all_vacancies(self):
        saver = JSONSaver()
        saver.vacancies = [{"title": "Vacancy 1", "link": "http://example.com/1"}]
        all_vacancies = saver.get_all_vacancies()
        self.assertEqual(len(all_vacancies), 1)
        self.assertEqual(all_vacancies[0]["title"], "Vacancy 1")


if __name__ == "__main__":
    unittest.main()
