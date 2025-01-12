class Vacancy:
    __slots__ = ('title', 'salary', 'requirements', 'responsibilities', 'url')

    def __init__(self, title, salary, requirements, responsibilities, url=None):
        self.title = title
        self.salary = salary if salary else "Зарплата не указана"
        self.requirements = requirements
        self.responsibilities = responsibilities
        self.url = url

    def to_dict(self):
        return {"name": self.title, "link": self.url, "salary": self.salary}

    def __lt__(self, other):
        return self.get_salary() < other.get_salary()

    def __eq__(self, other):
        return self.get_salary() == other.get_salary()

    def get_salary(self):
        try:
            if " - " in self.salary:
                from_salary, to_salary = map(
                    lambda x: int(x.split()[0]) if x.split()[0].isdigit() else 0,
                    self.salary.split(" - "),
                )
                return from_salary
            else:
                return (
                    int(self.salary.split()[0])
                    if self.salary.split()[0].isdigit()
                    else 0
                )
        except ValueError:
            return 0  # Если зарплата не указана правильно, возвращаем 0

    @staticmethod
    def cast_to_object_list(vacancies_data):
        vacancies_list = []
        for item in vacancies_data:
            salary_from = item["salary"].get("from", 0)
            salary_to = item["salary"].get("to", 0)
            salary_currency = item["salary"].get("currency", "")
            salary = (
                f"{salary_from} - {salary_to} {salary_currency}".strip()
                if salary_from or salary_to
                else None
            )

            vacancy = Vacancy(
                title=item.get("name"),
                url=f"https://hh.ru/vacancy/{item['id']}",
                salary=salary,
                requirements=item.get("description", "Нет описания"),
                responsibilities=item.get("responsibilities", "Нет обязанностей"),
            )
            vacancies_list.append(vacancy)
        return vacancies_list

    @staticmethod
    def filter_vacancies(vacancies, filter_words):
        return [
            v
            for v in vacancies
            if any(word.lower() in v.title.lower() for word in filter_words)
        ]

    @staticmethod
    def get_vacancies_by_salary(vacancies, salary_range):
        salary_from, salary_to = map(int, salary_range.split("-"))
        filtered_vacancies = []
        for v in vacancies:
            try:
                if " - " in v.salary:
                    from_salary, to_salary = map(
                        lambda x: int(x.split()[0]) if x.split()[0].isdigit() else 0,
                        v.salary.split(" - "),
                    )
                else:
                    from_salary = to_salary = (
                        int(v.salary.split()[0]) if v.salary.split()[0].isdigit() else 0
                    )

                if from_salary >= salary_from and (
                    to_salary == 0 or to_salary <= salary_to
                ):
                    filtered_vacancies.append(v)
            except ValueError:
                continue  # Пропустим вакансии с некорректными зарплатами
        return filtered_vacancies

    @staticmethod
    def sort_vacancies(vacancies):
        return sorted(
            vacancies,
            key=lambda v: (
                int(v.salary.split()[0]) if v.salary.split()[0].isdigit() else 0
            ),
        )

    @staticmethod
    def get_top_vacancies(vacancies, top_n):
        return vacancies[:top_n]

    @staticmethod
    def print_vacancies(vacancies):
        for i, item in enumerate(vacancies, start=1):
            print(f"{i}: {item.title} - {item.salary} ({item.url})")
