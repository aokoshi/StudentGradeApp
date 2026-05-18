from typing import Iterable
from models import Student, Course, Grade
from .gpa_calculator import gpa_for_all


def top_students(students: Iterable[Student],
                 courses_by_code: dict[str, Course],
                 n: int = 5) -> list[tuple[Student, float]]:
    ranked = sorted(gpa_for_all(students, courses_by_code),
                    key=lambda pair: pair[1],
                    reverse=True)
    return ranked[:n]


def failing_students(students: Iterable[Student],
                     courses_by_code: dict[str, Course],
                     threshold: float = 2.0) -> list[tuple[Student, float]]:
    return list(filter(lambda pair: pair[1] < threshold,
                       gpa_for_all(students, courses_by_code)))


def course_averages(grades: Iterable[Grade]) -> dict[str, float]:
    """Average raw score per course code. Dict lookup → O(n) total."""
    totals: dict[str, list[float]] = {}
    for g in grades:
        totals.setdefault(g.course_code, []).append(g.score)
    return {code: round(sum(scores) / len(scores), 2)
            for code, scores in totals.items()}
