from abc import ABC, abstractmethod

import requests


class BaseAPI(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_vacancies(self, query, params=None):
        pass


class HeadHunterAPI(BaseAPI):
    def __init__(self):
        self.base_url = "https://api.hh.ru/"
        self.vacancies_url = self.base_url + "vacancies"
        self.headers = {"User-Agent": "SkyApp 1.0 (karimov.jalil@mail.ru)"}

    def connect(self):
        response = requests.get(self.vacancies_url, headers=self.headers)
        return response.status_code == 200

    def get_vacancies(self, query, params=None):
        if params is None:
            params = {}
        params["text"] = query
        params["only_with_salary"] = True

        response = requests.get(self.vacancies_url, params=params, headers=self.headers)
        response.raise_for_status()  # Вызывает исключение, если статус не 2xx
        data = response.json()
        return {"items": data.get("items", [])}


if __name__ == "__main__":
    try:
        hh_api = HeadHunterAPI()

        if hh_api.connect():
            print("Подключение к API успешно!")

            vacancies = hh_api.get_vacancies("Python")["items"]

            print(f"Получено {len(vacancies)} вакансий.")
            for i, item in enumerate(vacancies, start=1):
                salary = item.get("salary")
                salary_info = (
                    f"{salary['from']} - {salary['to']} {salary['currency']}"
                    if salary
                    else "Не указана"
                )
                print(f"{i}: {item['name']} - {salary_info}")
        else:
            print("Не удалось подключиться к API.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при обращении к API: {e}")
