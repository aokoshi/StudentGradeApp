# StudentGradeAPP v2

A professional console application for managing students, courses and grades —
built for **Introduction to Programming 2 (Python)** at AITU.

This is the enhanced version of *Case 2: Student Grade Management System* from
the final project brief. It uses **SQLite** for persistent storage and the
**rich** library for a colorful, polished terminal interface.

---

## Features

### Student management
- List all students with **ID, Full Name, # Grades, # Enrolled Courses, cGPA**.
- *Student Profile* page: personal info, overall cGPA, plus a per-course
  breakdown (trimester scores, final %, letter grade, course GPA).
- Add / update / delete students with input validation.

### Course management
- List all courses with **ID, Name, Credits, Hours, # Enrolled Students**.
- *Course Details* page: every enrolled student with their T1/T2/T3 GPA and
  final course GPA.
- Add / update / delete courses.

### Grading workflow (the required flow)
`Main menu → Add/Update Grades →`
1. Display **all students** in a table.
2. Prompt for a **Student ID**.
3. Display **only the courses that student is enrolled in**.
4. Prompt for a **Course ID** (validated against that filtered list).
5. Prompt for the **trimester** (1/2/3) and **score** (0–100).
6. Update the database and confirm.

### Reports
- Top-N students by cGPA.
- Full student / course listings.

### UX touches
- **Breadcrumbs** at the top of every screen (e.g. `Home › Students › Details`).
- **Success / error / cancellation** messages for every action.
- Robust validation — typing letters where a number is expected never crashes
  the app.

---

## GPA scale (AITU standard, 100-point → 4.0)

| Score | Letter | GPA |
|-------|--------|-----|
| 95–100 | A   | 4.00 |
| 90–94  | A-  | 3.67 |
| 85–89  | B+  | 3.33 |
| 80–84  | B   | 3.00 |
| 75–79  | B-  | 2.67 |
| 70–74  | C+  | 2.33 |
| 65–69  | C   | 2.00 |
| 60–64  | C-  | 1.67 |
| 55–59  | D+  | 1.33 |
| 50–54  | D   | 1.00 |
| < 50   | F   | 0.00 |

- **Final course score** = mean of the recorded trimester scores.
- **Cumulative GPA (cGPA)** = `Σ(course_gpa × credits) / Σ(credits)`, computed
  only over courses that have at least one recorded score.

---

## Project structure

```
StudentGradeAPP_v2/
├── main.py                  # Entry point
├── requirements.txt
├── README.md
├── data/                    # SQLite DB lives here (auto-created)
├── models/                  # Domain classes (OOP)
│   ├── person.py            # Abstract base (inheritance demo)
│   ├── student.py           # Person → Student (polymorphism via role())
│   ├── course.py
│   └── enrollment.py
├── database/
│   └── db_manager.py        # SQLite wrapper + schema bootstrap
├── services/                # Business logic
│   ├── student_service.py
│   ├── course_service.py
│   └── grade_service.py
├── ui/                      # rich-based UI
│   ├── console.py           # Banner, prompts, success/error helpers
│   ├── views.py             # Tables & panels
│   └── menus.py             # Menu loops + actions
├── utils/
│   ├── gpa.py               # Score ↔ letter ↔ GPA, cGPA math
│   ├── validators.py        # Regex + bounded-int parsing
│   └── decorators.py        # @confirm_action, @catch_errors
└── tests/
    ├── test_gpa.py
    └── test_validators.py
```

---

## How to run

### 1. Requirements

- **Python 3.10+** (uses `int | None` syntax)

### 2. Install dependencies

```bash
cd StudentGradeAPP_v2
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the app

```bash
python main.py
```

The SQLite database `data/students.db` is created automatically on first run.

### 4. Run the tests

```bash
python -m unittest discover -s tests -v
```

---

## How the assignment requirements are covered

| Brief requirement | Where it lives |
|---|---|
| 3–5 classes | `Person`, `Student`, `Course`, `Enrollment`, plus 3 service classes |
| Encapsulation | dataclasses + private DB connection inside `Database` |
| Inheritance  | `Student(Person)` |
| Polymorphism | `Person.role()` overridden by `Student.role()` |
| Lists, dicts, tuples, sets | results lists, `GRADE_TABLE` tuples, `valid_course_ids` set, services use dict-style row mapping |
| File handling | SQLite persistent storage (`data/students.db`) |
| Modules + structure | `models/`, `database/`, `services/`, `ui/`, `utils/`, `tests/` |
| Unit testing | `tests/test_gpa.py`, `tests/test_validators.py` (`unittest`) |
| Algorithmic efficiency | Set-based membership check in the grading workflow (O(1) instead of O(n)); single-pass weighted cGPA |
| Advanced features | **Decorators** (`@confirm_action`, `@catch_errors`), **generators** (`StudentService.iter_all`), **lambda + filter** (top-students report), **regex** (email + name validators) |

---

## Team members

> Replace this section with your real team before submitting.

- Member 1 — *role: e.g. database layer + services*
- Member 2 — *role: e.g. UI / menu flow*
- Member 3 — *role: e.g. GPA / validators / tests*
- Member 4 — *role: e.g. models / docs / presentation*
