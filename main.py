from src.files import JSONSaver
from src.vacancy import Vacancy
from src.api import HeadHunterAPI

# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("Python")

# Проверка, что данные получены корректно
if 'items' in hh_vacancies:
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies['items'])
else:
    print("Ошибка: данные о вакансиях не получены.")
    vacancies_list = []

# Сохранение информации о вакансиях в файл
json_saver = JSONSaver()
for vacancy in vacancies_list:
    json_saver.add_vacancy(vacancy)

# Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ["HeadHunter"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")  # Пример: 100000 - 150000

    filtered_vacancies = Vacancy.filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = Vacancy.get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = Vacancy.sort_vacancies(ranged_vacancies)
    top_vacancies = Vacancy.get_top_vacancies(sorted_vacancies, top_n)
    Vacancy.print_vacancies(top_vacancies)

if __name__ == "__main__":
    user_interaction()
