from .person import Person
from .grade import Grade


class Student(Person):
    def __init__(self, person_id: int, name: str, group: str = ""):
        super().__init__(person_id, name)
        self._group = group
        self._grades: list[Grade] = []

    @property
    def group(self) -> str:
        return self._group

    @property
    def grades(self) -> list[Grade]:
        return list(self._grades)

    def add_grade(self, grade: Grade) -> None:
        if not isinstance(grade, Grade):
            raise TypeError("expected Grade instance")
        self._grades.append(grade)

    def courses(self) -> set[str]:
        return {g.course_code for g in self._grades}

    def role(self) -> str:
        return "student"
