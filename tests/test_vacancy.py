import unittest

from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):

    def setUp(self):
        self.vacancy1 = Vacancy(
            "Developer", "1000", "Python, Django", "Develop web applications"
        )
        self.vacancy2 = Vacancy(
            "Senior Developer", "2000 - 2500", "Python, Django", "Lead a team"
        )
        self.vacancy3 = Vacancy(
            "Junior Developer", "800", "Python", "Assist in projects"
        )
        self.vacancy_invalid = Vacancy(
            "Intern", "not a number", "No requirements", "No responsibilities"
        )

    def test_vacancy_initialization(self):
        self.assertEqual(self.vacancy1.title, "Developer")
        self.assertEqual(self.vacancy1.salary, "1000")
        self.assertEqual(self.vacancy1.requirements, "Python, Django")
        self.assertEqual(self.vacancy1.responsibilities, "Develop web applications")
        self.assertIsNone(self.vacancy1.url)

    def test_to_dict(self):
        expected_dict = {"name": "Developer", "link": None, "salary": "1000"}
        self.assertEqual(self.vacancy1.to_dict(), expected_dict)

    def test_get_salary(self):
        self.assertEqual(self.vacancy1.get_salary(), 1000)
        self.assertEqual(self.vacancy2.get_salary(), 2000)
        self.assertEqual(self.vacancy3.get_salary(), 800)
        self.assertEqual(self.vacancy_invalid.get_salary(), 0)

    def test_vacancy_comparisons(self):
        self.assertTrue(self.vacancy1 < self.vacancy2)
        self.assertFalse(self.vacancy2 < self.vacancy1)
        self.assertFalse(self.vacancy1 == self.vacancy2)
        self.assertTrue(self.vacancy1 == self.vacancy1)

    def test_cast_to_object_list(self):
        vacancies_data = [
            {
                "id": 1,
                "name": "Developer",
                "salary": {"from": 1000, "to": 1500, "currency": ""},
                "description": "Python developer",
                "responsibilities": "Develop applications",
            },
            {
                "id": 2,
                "name": "Manager",
                "salary": {"from": 2000, "to": 2500, "currency": ""},
                "description": "Management role",
                "responsibilities": "Manage projects",
            },
        ]
        vacancies = Vacancy.cast_to_object_list(vacancies_data)
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0].title, "Developer")
        self.assertEqual(vacancies[1].title, "Manager")

    def test_filter_vacancies(self):
        vacancy_list = [self.vacancy1, self.vacancy2, self.vacancy3]
        filtered = Vacancy.filter_vacancies(vacancy_list, ["Developer"])
        self.assertEqual(len(filtered), 3)

    def test_get_vacancies_by_salary(self):
        vacancy_list = [self.vacancy1, self.vacancy2, self.vacancy3]
        filtered = Vacancy.get_vacancies_by_salary(vacancy_list, "800-1500")
        self.assertEqual(len(filtered), 2)

    def test_sort_vacancies(self):
        vacancy_list = [self.vacancy2, self.vacancy1, self.vacancy3]
        sorted_vacancies = Vacancy.sort_vacancies(vacancy_list)
        self.assertEqual(sorted_vacancies[0], self.vacancy3)
        self.assertEqual(sorted_vacancies[1], self.vacancy1)
        self.assertEqual(sorted_vacancies[2], self.vacancy2)

    def test_get_top_vacancies(self):
        vacancy_list = [self.vacancy1, self.vacancy2, self.vacancy3]
        top_vacancies = Vacancy.get_top_vacancies(vacancy_list, 2)
        self.assertEqual(len(top_vacancies), 2)
        self.assertEqual(top_vacancies[0], self.vacancy1)
        self.assertEqual(top_vacancies[1], self.vacancy2)


if __name__ == "__main__":
    unittest.main()
