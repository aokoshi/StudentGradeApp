# StudentGradeAPP v2

A professional console application for managing students, courses and grades —
built for **Introduction to Programming 2 (Python)** at AITU.

This is the enhanced version of *Case 2: Student Grade Management System* from
the final project brief. It uses **SQLite** for persistent storage, the
**rich** library for a polished terminal interface, and supports exporting
reports to **CSV** and **JSON** files.

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

### Grading workflow
`Main menu → Add/Update Grades →`
1. Display **all students** in a table.
2. Prompt for a **Student ID**.
3. Display **only the courses that student is enrolled in**.
4. Prompt for a **Course ID** (validated against that filtered list).
5. Prompt for the **trimester** (1/2/3) and **score** (0–100).
6. Update the database and confirm.

### Reports & **file exports (CSV / JSON)**
From the **Reports** menu:
- *Top-N students by cGPA*
- *Full student listing*
- *Full course listing*
- **Export reports to CSV** → 3 files in a fresh timestamped folder
- **Export reports to JSON** → 1 combined snapshot in a fresh timestamped folder

#### Where exported files go

Everything is written under the project's `exports/` folder. Each export run
creates its own subfolder named with the current timestamp, so reports never
overwrite each other:

```
exports/
└── 2026-05-18_14-30-22/      ← created automatically on each export
    ├── students.csv          ← CSV export writes 3 files…
    ├── courses.csv
    ├── grades.csv
    └── full_report.json      ← …JSON export writes 1 combined file
```

When the export finishes the app prints the **full path** so you can find them
easily in your file manager.

#### What's in each file

**`students.csv`** — one row per student
```
student_id,first_name,last_name,email,course_count,grade_count,cgpa
1,Aizada,Tester,a@aitu.edu.kz,2,3,3.10
```

**`courses.csv`** — one row per course
```
course_id,name,credits,hours,student_count
1,Intro to Programming 2,3,60,1
2,Calculus I,4,90,1
```

**`grades.csv`** — one row per (student, course) enrollment
```
student_id,full_name,course_id,course_name,credits,t1,t2,t3,final_score,letter,gpa
1,Aizada Tester,1,Intro to Programming 2,3,92.0,88.0,,90.00,A-,3.67
1,Aizada Tester,2,Calculus I,4,75.0,,,75.00,B-,2.67
```

**`full_report.json`** — combined nested snapshot
```json
{
  "exported_at": "2026-05-18T14:30:22",
  "students": [
    {
      "id": 1,
      "full_name": "Aizada Tester",
      "email": "a@aitu.edu.kz",
      "cgpa": 3.10,
      "course_count": 2,
      "grade_count": 3,
      "enrollments": [
        {"course_id": 1, "course_name": "Intro to Programming 2",
         "credits": 3, "t1": 92.0, "t2": 88.0, "t3": null,
         "final_score": 90.0, "letter": "A-", "gpa": 3.67}
      ]
    }
  ],
  "courses": [
    {"id": 1, "name": "Intro to Programming 2",
     "credits": 3, "hours": 60, "student_count": 1}
  ]
}
```

### UX touches
- **Breadcrumbs** at the top of every screen (e.g. `Home › Students › Details`).
- **Success / error / cancellation** messages for every action.
- A **rich progress spinner** while exports are being written.
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
├── exports/                 # CSV / JSON reports land here (auto-created)
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
│   ├── grade_service.py
│   └── export_service.py    # CSV + JSON report writers
├── ui/                      # rich-based UI
│   ├── console.py           # Banner, prompts, success/error helpers
│   ├── views.py             # Tables & panels
│   └── menus.py             # Menu loops + actions + export action
├── utils/
│   ├── gpa.py               # Score ↔ letter ↔ GPA, cGPA math
│   ├── validators.py        # Regex + bounded-int parsing
│   └── decorators.py        # @confirm_action, @catch_errors
└── tests/
    ├── test_gpa.py
    ├── test_validators.py
    └── test_export.py
```

---

## How to run

### 1. Requirements

- **Python 3.10+** (uses `int | None` syntax)

### 2. Install dependencies

```bash
cd StudentGradeAPP_v3
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

The SQLite database `data/students.db` and the `exports/` folder are created
automatically on first run.

### 4. Run the tests

```bash
python -m unittest discover -s tests -v
```

---

## How the assignment requirements are covered

| Brief requirement | Where it lives |
|---|---|
| 3–5 classes | `Person`, `Student`, `Course`, `Enrollment`, plus 4 service classes |
| Encapsulation | dataclasses + private DB connection inside `Database` |
| Inheritance  | `Student(Person)` |
| Polymorphism | `Person.role()` overridden by `Student.role()` |
| Lists, dicts, tuples, sets | results lists, `GRADE_TABLE` tuples, `valid_course_ids` set, services use dict-style row mapping |
| **File handling (CSV / JSON)** | `services/export_service.py` writes `exports/<timestamp>/{students,courses,grades}.csv` and `full_report.json`. Plus SQLite for persistent storage. |
| Modules + structure | `models/`, `database/`, `services/`, `ui/`, `utils/`, `tests/` |
| Unit testing | `tests/test_gpa.py`, `tests/test_validators.py`, `tests/test_export.py` (`unittest`) |
| Algorithmic efficiency | Set-based membership check in the grading workflow (O(1) instead of O(n)); single-pass weighted cGPA |
| Advanced features | **Decorators** (`@confirm_action`, `@catch_errors`), **generators** (`StudentService.iter_all`), **lambda + filter** (top-students report), **regex** (email + name validators) |

---

