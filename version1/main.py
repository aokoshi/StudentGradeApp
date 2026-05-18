"""Student Grade Management — console entry point.

Owned by Member 2 (integration). Wires together models, services, utils, and the
console UI.
"""
from pathlib import Path

from models import Student, Grade, Course, Admin
from services import top_students, failing_students, course_averages
from utils import load_grades_csv, save_grades_csv, load_json
from ui.console import menu, prompt, prompt_int, prompt_float, print_table

DATA_DIR = Path(__file__).parent / "data"
GRADES_CSV = DATA_DIR / "grades.csv"
COURSES_JSON = DATA_DIR / "courses.json"


def load_state():
    students = {}
    grades = []
    if GRADES_CSV.exists():
        students, grades = load_grades_csv(GRADES_CSV)

    courses_by_code = {}
    if COURSES_JSON.exists():
        for c in load_json(COURSES_JSON):
            courses_by_code[c["code"]] = Course(c["code"], c["title"], c["credits"])

    return students, grades, courses_by_code


def action_list_students(students, *_):
    rows = [[s.id, s.name, len(s.grades)] for s in students.values()]
    print_table(["ID", "Name", "# grades"], rows)


def action_add_student(students, *_):
    sid = prompt_int("Student ID")
    if sid in students:
        print(f"  student #{sid} already exists.")
        return
    name = prompt("Name")
    students[sid] = Student(sid, name)
    print(f"  added {name} (#{sid}).")


def action_add_grade(students, grades, courses_by_code):
    sid = prompt_int("Student ID")
    if sid not in students:
        print(f"  unknown student #{sid}.")
        return
    code = prompt("Course code")
    score = prompt_float("Score (0–100)")
    g = Grade(sid, code, score)
    students[sid].add_grade(g)
    grades.append(g)
    print(f"  recorded {code}={score} for {students[sid].name}.")


def action_top_students(students, _grades, courses_by_code):
    n = prompt_int("How many top students")
    rows = [[s.name, gpa] for s, gpa in top_students(students.values(), courses_by_code, n)]
    print_table(["Name", "GPA"], rows)


def action_failing(students, _grades, courses_by_code):
    rows = [[s.name, gpa] for s, gpa in failing_students(students.values(), courses_by_code)]
    if not rows:
        print("  no failing students. ")
        return
    print_table(["Name", "GPA"], rows)


def action_averages(_students, grades, _courses):
    avgs = course_averages(grades)
    print_table(["Course", "Average"], [[c, a] for c, a in sorted(avgs.items())])


def action_save(students, *_):
    save_grades_csv(GRADES_CSV, students)
    print(f"  saved to {GRADES_CSV}")


def main():
    admin = Admin(1, "Demo Admin", "admin", "admin")
    print("=== Student Grade Manager ===")
    if not admin.verify(prompt("Username"), prompt("Password")):
        print("Invalid credentials. Bye.")
        return

    students, grades, courses_by_code = load_state()

    actions = [
        ("List students", action_list_students),
        ("Add student", action_add_student),
        ("Add grade", action_add_grade),
        ("Top students", action_top_students),
        ("Failing students", action_failing),
        ("Course averages", action_averages),
        ("Save to CSV", action_save),
        ("Exit", None),
    ]

    while True:
        choice = menu("Main menu", [label for label, _ in actions])
        label, fn = actions[choice]
        if fn is None:
            print("Bye.")
            return
        try:
            fn(students, grades, courses_by_code)
        except Exception as e:
            print(f"  error: {e}")


if __name__ == "__main__":
    main()
