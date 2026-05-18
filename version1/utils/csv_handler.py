import csv
from pathlib import Path
from models import Student, Grade


def load_grades_csv(path: str | Path) -> tuple[dict[int, Student], list[Grade]]:
    """Load CSV with columns: student_id,name,course,grade.

    Returns (students_by_id, all_grades).
    """
    students: dict[int, Student] = {}
    grades: list[Grade] = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                sid = int(row["student_id"])
            except (KeyError, ValueError):
                raise ValueError(f"invalid student_id row: {row}")

            if sid not in students:
                students[sid] = Student(sid, row["name"])

            try:
                score = float(row["grade"])
            except (KeyError, ValueError):
                raise ValueError(f"invalid grade row: {row}")

            grade = Grade(sid, row["course"], score)
            students[sid].add_grade(grade)
            grades.append(grade)

    return students, grades


def save_grades_csv(path: str | Path, students: dict[int, Student]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["student_id", "name", "course", "grade"])
        for student in students.values():
            for g in student.grades:
                writer.writerow([student.id, student.name, g.course_code, g.score])
