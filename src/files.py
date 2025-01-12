import json
import os


class JSONSaver:
    def __init__(self, file_path=None):
        if file_path is None:
            # Создаем путь к файлу относительно текущего файла
            self.file_path = os.path.join(
                os.path.dirname(__file__), "../data/vacancies.json"
            )
        else:
            self.file_path = file_path
        self.vacancies = self.load_vacancies()

    def load_vacancies(self):
        if not os.path.exists(self.file_path):
            return []  # Возвращаем пустой список, если файл не существует
        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if isinstance(
                    data, list
                ):  # Убедитесь, что загруженные данные - это список
                    return data
                else:
                    return (
                        []
                    )  # Если данные не в формате списка, возвращаем пустой список
            except json.JSONDecodeError:
                return (
                    []
                )  # Если есть ошибка при декодировании, возвращаем пустой список

    def save_vacancies(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                self.vacancies,
                file,
                default=lambda o: o.__dict__,
                ensure_ascii=False,
                indent=4,
            )

    def add_vacancy(self, vacancy_dict):
        self.vacancies.append(vacancy_dict)  # Добавляем словарь в список
        self.save_vacancies()

    def delete_vacancy(self, vacancy):
        self.vacancies = [v for v in self.vacancies if v["link"] != vacancy.link]
        self.save_vacancies()

    def get_all_vacancies(self):
        return self.vacancies
