# Student Grade Management System

Console application for managing students, courses, and grades.
Built in pure Python (stdlib only) — no third-party dependencies.

Final project for **Introduction to Programming 2** (AITU, Spring 2026).

## How to run

```bash
# Requires Python 3.10+
python main.py
```

Demo login: `admin` / `admin`.

## Run the tests

```bash
python -m unittest discover tests
```

## Project structure

```
StudentGradeApp/
├── main.py              # console entry — menu loop
├── README.md
├── TASKS.md             # per-member commit plan
├── requirements.txt     # empty — stdlib only
├── data/
│   ├── grades.csv       # sample input (CSV format from spec)
│   └── courses.json     # course catalog
├── models/              # OOP layer
│   ├── person.py        #   base class
│   ├── student.py       #   inherits Person
│   ├── admin.py         #   inherits Person, has login
│   ├── course.py
│   └── grade.py
├── services/            # business logic
│   ├── gpa_calculator.py
│   ├── report_generator.py
│   └── decorators.py    # @log_call, @timed
├── utils/               # I/O & helpers
│   ├── csv_handler.py
│   ├── json_handler.py
│   └── validators.py    # regex-based
├── ui/
│   └── console.py       # menus, prompts, tables
└── tests/               # unit tests (everyone tests their own module)
    ├── test_models.py
    ├── test_services.py
    └── test_utils.py
```

## Requirements coverage

| Requirement (PDF §) | Where it lives |
|---|---|
| 3.1 Functions, control flow, error handling | throughout — try/except in `main.py` action dispatch |
| 3.2 OOP — 3+ classes, encapsulation, inheritance, polymorphism | `models/` — `Person` base, `Student`/`Admin` subclasses, `role()` is polymorphic, private `_id`/`_name` |
| 3.3 Collections: list, dict, tuple, set | grades list, `students` dict, `LETTER_BOUNDS` tuple, `student.courses()` set |
| 3.4 File handling — CSV + JSON | `utils/csv_handler.py`, `utils/json_handler.py`, sample files in `data/` |
| 3.5 Modular structure | `models/ services/ utils/ ui/ tests/` |
| 3.6 Unit testing (`unittest`) | `tests/` — 16+ tests |
| 3.7 Algorithmic efficiency | `courses_by_code` dict lookup (O(1)) instead of nested loops |
| 3.8 Advanced features | Decorators (`services/decorators.py`), generator (`gpa_for_all`), lambda (`top_students` sort key + `filter` in `failing_students`), regex (`utils/validators.py`) |
