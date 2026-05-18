from typing import Iterable, Iterator
from models import Student, Course
from .decorators import log_call


@log_call
def calculate_gpa(student: Student, courses_by_code: dict[str, Course]) -> float:
    """Credit-weighted GPA on a 4.0 scale."""
    total_points = 0.0
    total_credits = 0
    for g in student.grades:
        course = courses_by_code.get(g.course_code)
        if course is None:
            continue
        total_points += g.gpa_points * course.credits
        total_credits += course.credits
    if total_credits == 0:
        return 0.0
    return round(total_points / total_credits, 2)


def gpa_for_all(students: Iterable[Student],
                courses_by_code: dict[str, Course]) -> Iterator[tuple[Student, float]]:
    """Generator — yields (student, gpa) one at a time (memory-efficient for large datasets)."""
    for s in students:
        yield s, calculate_gpa(s, courses_by_code)
