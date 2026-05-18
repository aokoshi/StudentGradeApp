# Step-by-step instructions for all team members

> Audience: 4 students working on the ITP2 final project (Student Grade Management System, console app).
> This doc tells **each member** exactly what to do, file by file, commit by commit.

## Why this matters

The assignment **penalises** projects where only 1–2 people commit. The graders look at `git log` and check that all four names appear with meaningful changes. So:

- Every member **must commit from their own machine** with their own Git identity.
- Do **not** copy-paste someone else's code in one big commit.
- Each commit should be small enough that the title alone explains what changed.

Target: **~8 commits per person × 4 people = ~32 commits total**.

## How to use this doc

There is a reference implementation already in this folder (from planning sessions). **Do not push it as-is.** Instead:

1. The team leader resets the working code to **empty stubs** (instructions in Phase 0 below).
2. Each member follows their section, recreating their slice commit by commit.
3. Use the reference implementation only to peek at if you get stuck.

---

## Phase 0 — One-time team setup (team leader does this once)

1. Push the empty scaffold to GitHub (without the implementation code), e.g.:
   ```powershell
   cd C:\Users\User\StudentGradeApp
   # Reset implementations back to stubs (keep folder/file structure, blank the bodies):
   # (Easiest: delete the .py file contents except the module docstring, then commit.)
   git init
   git add .
   git commit -m "chore: initial empty scaffold"
   gh repo create StudentGradeApp --public --source=. --push
   ```
2. In GitHub repo settings → Collaborators → invite the other 3 teammates.
3. Share this `INSTRUCTIONS.md` with them.

---

## Phase 1 — Per-member one-time setup (each member does this once on their own machine)

1. Install Git and Python 3.10+ if not already.
2. Configure your Git identity (use your real name and AITU email so it's recognised):
   ```powershell
   git config --global user.name "Your Full Name"
   git config --global user.email "YOUR_ID@astanait.edu.kz"
   ```
3. Clone the repo:
   ```powershell
   git clone https://github.com/<team-leader>/StudentGradeApp.git
   cd StudentGradeApp
   ```
4. Create **your own branch** (replace `<area>` with your area — `services`, `models`, `utils`, or `ui`):
   ```powershell
   git checkout -b feat/<area>
   ```
5. Confirm Python works: `python --version` (should be 3.10+).

---

## Phase 2 — The work, member by member

Each commit below shows:
- **Files touched**
- **What to write** (signatures + key logic hints — not the full code)
- **Commit message** (use this exact wording so the history looks consistent)

After each commit, push your branch:
```powershell
git add <files>
git commit -m "<message>"
git push origin feat/<area>
```

---

### MEMBER 1 — Services (HARD)

**Branch:** `feat/services`
**Owns:** `services/__init__.py`, `services/gpa_calculator.py`, `services/report_generator.py`, `services/decorators.py`, `tests/test_services.py`

#### Commit 1 — `services: scaffold package with __init__.py exports`

**Files:** `services/__init__.py`, `services/gpa_calculator.py`, `services/report_generator.py`, `services/decorators.py`

Create stubs so the imports in `main.py` don't crash. Each function raises `NotImplementedError` for now.

```python
# services/gpa_calculator.py
def calculate_gpa(student, courses_by_code): raise NotImplementedError
def gpa_for_all(students, courses_by_code): raise NotImplementedError

# services/report_generator.py
def top_students(students, courses_by_code, n): raise NotImplementedError
def failing_students(students, courses_by_code): raise NotImplementedError
def course_averages(grades): raise NotImplementedError

# services/decorators.py
def log_call(fn): return fn
def timed(fn): return fn

# services/__init__.py
from .gpa_calculator import calculate_gpa, gpa_for_all
from .report_generator import top_students, failing_students, course_averages
from .decorators import log_call, timed
```

#### Commit 2 — `services: add @log_call decorator`

**File:** `services/decorators.py`

Replace the `log_call` stub with a real decorator that prints the function name and arguments each time it's called. Use `functools.wraps` so the wrapped function keeps its original name.

```python
import functools
def log_call(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"  [log] {fn.__name__}({len(args)} args)")
        return fn(*args, **kwargs)
    return wrapper
```

#### Commit 3 — `services: add @timed decorator using time.perf_counter`

**File:** `services/decorators.py`

Add a `timed` decorator that measures execution time of any function. This is the **second advanced Python feature** (decorators) that satisfies requirement 3.8.

```python
import time, functools
def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"  [timed] {fn.__name__}: {(time.perf_counter()-t0)*1000:.2f} ms")
    return wrapper
```

#### Commit 4 — `services: implement calculate_gpa (credit-weighted, 4.0 scale)`

**File:** `services/gpa_calculator.py`

Compute weighted GPA. For each grade the student has, look up the course's credits via the `courses_by_code` dictionary (**O(1) lookup** — justify this in your defense). Multiply each grade's GPA value by the course credits, sum, divide by total credits.

```python
def calculate_gpa(student, courses_by_code):
    total_points = 0.0
    total_credits = 0
    for g in student.grades:
        course = courses_by_code.get(g.course_code)
        if course is None:
            continue
        total_points += g.gpa * course.credits
        total_credits += course.credits
    return round(total_points / total_credits, 2) if total_credits else 0.0
```

#### Commit 5 — `services: extract gpa_for_all as generator for lazy evaluation`

**File:** `services/gpa_calculator.py`

Add a **generator** that yields `(student, gpa)` pairs lazily. This satisfies the "generators vs lists, memory considerations" line from the requirements doc.

```python
def gpa_for_all(students, courses_by_code):
    for s in students:
        yield s, calculate_gpa(s, courses_by_code)
```

#### Commit 6 — `services: add top_students using sorted + lambda key`

**File:** `services/report_generator.py`

Sort pairs by GPA descending, return top N. Uses **lambda** (covers the lambda/map/filter advanced feature).

```python
from .gpa_calculator import gpa_for_all
def top_students(students, courses_by_code, n):
    pairs = list(gpa_for_all(students, courses_by_code))
    return sorted(pairs, key=lambda p: p[1], reverse=True)[:n]
```

#### Commit 7 — `services: add failing_students (filter) and course_averages`

**File:** `services/report_generator.py`

- `failing_students` uses Python's built-in `filter()` with a lambda to keep only students below 2.0 GPA.
- `course_averages` iterates over all grades and builds a dict `{course_code → average_score}`.

```python
def failing_students(students, courses_by_code):
    pairs = gpa_for_all(students, courses_by_code)
    return list(filter(lambda p: p[1] < 2.0, pairs))

def course_averages(grades):
    sums, counts = {}, {}
    for g in grades:
        sums[g.course_code] = sums.get(g.course_code, 0.0) + g.score
        counts[g.course_code] = counts.get(g.course_code, 0) + 1
    return {code: round(sums[code]/counts[code], 2) for code in sums}
```

#### Commit 8 — `tests: cover GPA edge cases, top-N order, course averages`

**File:** `tests/test_services.py`

Use `unittest`. Write at least 4 tests:
1. GPA of a student with no grades = 0.0
2. GPA of a student with all A's = 4.0
3. `top_students(..., n=2)` returns exactly 2 entries sorted by GPA descending
4. `course_averages` correctly averages multiple grades for the same course

Skeleton:
```python
import unittest
from models import Student, Grade, Course
from services import calculate_gpa, top_students, course_averages

class TestServices(unittest.TestCase):
    def setUp(self):
        self.courses = {"M": Course("M", "Math", 3), "P": Course("P", "Phys", 4)}
        self.s = Student(1, "X")
        self.s.add_grade(Grade(1, "M", 95))  # A → 4.0 × 3
        self.s.add_grade(Grade(1, "P", 75))  # C → 2.0 × 4
    def test_calculate_gpa(self):
        self.assertAlmostEqual(calculate_gpa(self.s, self.courses), 2.86, places=2)
    # ... add 3 more tests
```

---

### MEMBER 2 — Models + integration (HARD)

**Branch:** `feat/models`
**Owns:** `models/*.py`, `main.py`, `tests/test_models.py`

#### Commit 1 — `models: add Person base class with encapsulated id/name`

**File:** `models/person.py`

Base class with private `_id` and `_name`, exposed via read-only `@property`. Validate that name is non-empty (covers the error-handling requirement).

```python
class Person:
    def __init__(self, person_id: int, name: str):
        if not name or not name.strip():
            raise ValueError("name must be non-empty")
        self._id = int(person_id)
        self._name = name.strip()
    @property
    def id(self): return self._id
    @property
    def name(self): return self._name
    def role(self): return "person"          # for polymorphism
    def __repr__(self): return f"{type(self).__name__}(id={self._id}, name={self._name!r})"
```

#### Commit 2 — `models: add Student subclass with grades list and courses set`

**File:** `models/student.py`

Inherits from `Person`. Stores a **list** of grades (order matters, duplicates ok) and a **set** of course codes (uniqueness matters). This is the **justification for two different data structures** the requirements ask for.

```python
from .person import Person
class Student(Person):
    def __init__(self, person_id, name):
        super().__init__(person_id, name)
        self.grades = []
        self.courses = set()
    def add_grade(self, grade):
        self.grades.append(grade)
        self.courses.add(grade.course_code)
    def role(self): return "student"          # polymorphism override
```

#### Commit 3 — `models: add Admin subclass with verify(username, password)`

**File:** `models/admin.py`

```python
from .person import Person
class Admin(Person):
    def __init__(self, person_id, name, username, password):
        super().__init__(person_id, name)
        self._username = username
        self._password = password
    def verify(self, username, password):
        return username == self._username and password == self._password
    def role(self): return "admin"
```

#### Commit 4 — `models: add Course with __eq__ / __hash__ on code`

**File:** `models/course.py`

Equality and hashing by `code` only, so `Course` objects work correctly when stored in `set` or used as `dict` keys.

```python
class Course:
    def __init__(self, code, title, credits):
        self.code = code
        self.title = title
        self.credits = int(credits)
    def __eq__(self, other):
        return isinstance(other, Course) and self.code == other.code
    def __hash__(self):
        return hash(self.code)
    def __repr__(self):
        return f"Course({self.code} {self.title}, {self.credits}cr)"
```

#### Commit 5 — `models: add Grade with letter/GPA mapping (LETTER_BOUNDS tuple)`

**File:** `models/grade.py`

Class-level **tuple** `LETTER_BOUNDS` holds the score → letter → GPA mapping. Tuples are immutable, which justifies the choice over a list (won't be modified).

```python
class Grade:
    LETTER_BOUNDS = (
        (90, "A", 4.0),
        (80, "B", 3.0),
        (70, "C", 2.0),
        (60, "D", 1.0),
        (0,  "F", 0.0),
    )
    def __init__(self, student_id, course_code, score):
        if not 0 <= score <= 100:
            raise ValueError("score must be 0..100")
        self.student_id = int(student_id)
        self.course_code = course_code
        self.score = float(score)
    @property
    def letter(self):
        for threshold, letter, _ in self.LETTER_BOUNDS:
            if self.score >= threshold:
                return letter
    @property
    def gpa(self):
        for threshold, _, gpa in self.LETTER_BOUNDS:
            if self.score >= threshold:
                return gpa
```

#### Commit 6 — `models: re-export everything from __init__.py`

**File:** `models/__init__.py`

```python
from .person import Person
from .student import Student
from .admin import Admin
from .course import Course
from .grade import Grade
__all__ = ["Person", "Student", "Admin", "Course", "Grade"]
```

#### Commit 7 — `main: wire models + services + utils into console menu loop`

**File:** `main.py`

Build the menu loop. It:
1. Asks for admin login (uses `Admin.verify`)
2. Loads grades.csv and courses.json
3. Shows a numbered menu (List, Add student, Add grade, Top N, Failing, Averages, Save, Exit)
4. Dispatches to an action function, wrapped in `try/except` so errors don't crash the app

Use the dict `actions = [("List students", action_list_students), ...]` pattern. Each action takes `(students, grades, courses_by_code)`. See the reference `main.py` in the repo for the structure.

#### Commit 8 — `tests: cover model construction, polymorphism, validation`

**File:** `tests/test_models.py`

At least 4 tests:
1. `Student(1, "Alice").role() == "student"` (polymorphism — overrides `Person.role`)
2. `Course("M", "Math", 3) == Course("M", "Algebra", 4)` (equality by code only)
3. `Grade(1, "M", 89).letter == "B"` and `Grade(1, "M", 90).letter == "A"` (boundary)
4. `Person(1, "  ")` raises `ValueError` (input validation)

---

### MEMBER 3 — Utils + data (EASY)

**Branch:** `feat/utils`
**Owns:** `utils/*.py`, `data/*`, `tests/test_utils.py`

#### Commit 1 — `data: add sample grades.csv (8 rows, 4 students, 3 courses)`

**File:** `data/grades.csv`

```csv
student_id,name,course,grade
1,John Smith,MATH101,85
1,John Smith,CS101,92
1,John Smith,ENG101,78
2,Alice Brown,MATH101,90
2,Alice Brown,CS101,88
3,Bob Lee,MATH101,65
3,Bob Lee,CS101,72
4,Carol Wu,ENG101,95
```

#### Commit 2 — `data: add courses.json course catalog`

**File:** `data/courses.json`

```json
[
  {"code": "MATH101", "title": "Calculus I", "credits": 4},
  {"code": "CS101",   "title": "Intro to Programming", "credits": 3},
  {"code": "ENG101",  "title": "Academic English", "credits": 2}
]
```

#### Commit 3 — `utils: implement load_grades_csv (DictReader → Student + Grade objects)`

**File:** `utils/csv_handler.py`

Reads the CSV with `csv.DictReader`, builds a `dict[int, Student]` keyed by id (dict for **O(1) lookup** — justify in defense), and a flat `list[Grade]`. If a student appears in multiple rows, you only create them once.

```python
import csv
from models import Student, Grade

def load_grades_csv(path):
    students = {}
    grades = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid = int(row["student_id"])
            if sid not in students:
                students[sid] = Student(sid, row["name"])
            g = Grade(sid, row["course"], float(row["grade"]))
            students[sid].add_grade(g)
            grades.append(g)
    return students, grades
```

#### Commit 4 — `utils: implement save_grades_csv (DictWriter)`

**File:** `utils/csv_handler.py`

Walks each student's grades and writes one row per grade.

```python
def save_grades_csv(path, students):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "name", "course", "grade"])
        writer.writeheader()
        for s in students.values():
            for g in s.grades:
                writer.writerow({
                    "student_id": s.id, "name": s.name,
                    "course": g.course_code, "grade": g.score,
                })
```

#### Commit 5 — `utils: implement load_json / save_json helpers`

**File:** `utils/json_handler.py`

Thin wrappers around `json.load`/`json.dump`. Always pass `encoding="utf-8"` and `indent=2` for save.

```python
import json
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

Also update `utils/__init__.py` to re-export these names.

#### Commit 6 — `utils: regex validators for email, score range, course code`

**File:** `utils/validators.py`

This is the **regex advanced feature** (requirement 3.8).

```python
import re
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
COURSE_CODE_RE = re.compile(r"^[A-Z]{2,4}\d{3}$")

def is_email(s):       return bool(EMAIL_RE.match(s))
def is_course_code(s): return bool(COURSE_CODE_RE.match(s))
def is_score(x):       return 0 <= x <= 100
```

#### Commit 7 — `tests: csv roundtrip (save → load → assert equality)`

**File:** `tests/test_utils.py`

Save a known student dict to a temp CSV, load it back, verify the number of students and grades match. Use `tempfile` for the temp path.

```python
import unittest, tempfile, os
from pathlib import Path
from utils import load_grades_csv, save_grades_csv
from models import Student, Grade

class TestCsvRoundtrip(unittest.TestCase):
    def test_roundtrip(self):
        students = {1: Student(1, "A")}
        students[1].add_grade(Grade(1, "M", 85))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "g.csv"
            save_grades_csv(p, students)
            loaded, grades = load_grades_csv(p)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(len(grades), 1)
        self.assertEqual(grades[0].score, 85)
```

#### Commit 8 — `tests: validators (valid + invalid inputs)`

**File:** `tests/test_utils.py` (append a second test class)

```python
from utils.validators import is_email, is_course_code, is_score
class TestValidators(unittest.TestCase):
    def test_email(self):
        self.assertTrue(is_email("a@b.kz"))
        self.assertFalse(is_email("not-an-email"))
    def test_course_code(self):
        self.assertTrue(is_course_code("CS101"))
        self.assertFalse(is_course_code("cs1"))
    def test_score(self):
        self.assertTrue(is_score(0)); self.assertTrue(is_score(100))
        self.assertFalse(is_score(-1)); self.assertFalse(is_score(101))
```

---

### MEMBER 4 — Console UI + README (EASY)

**Branch:** `feat/ui`
**Owns:** `ui/console.py`, parts of `main.py` (action dispatch tweaks), `README.md` final pass

> Note: `main.py` is mostly owned by Member 2, but the **UI helpers** in `ui/console.py` are entirely yours. Coordinate via Pull Request comments so you don't step on each other's commits.

#### Commit 1 — `ui: scaffold console.py with prompt() helper`

**File:** `ui/console.py`

```python
def prompt(label: str) -> str:
    return input(f"{label}: ").strip()
```

#### Commit 2 — `ui: add prompt_int + prompt_float with retry-on-bad-input`

**File:** `ui/console.py`

Loops until the user types a valid number. This covers error handling for user input.

```python
def prompt_int(label):
    while True:
        try:
            return int(input(f"{label}: ").strip())
        except ValueError:
            print("  please enter a whole number.")

def prompt_float(label):
    while True:
        try:
            return float(input(f"{label}: ").strip())
        except ValueError:
            print("  please enter a number.")
```

#### Commit 3 — `ui: add print_table — minimal pretty 2D table printer`

**File:** `ui/console.py`

Calculates the widest cell per column, prints headers, a divider, then each row left-aligned.

```python
def print_table(headers, rows):
    cols = list(zip(headers, *rows)) if rows else [[h] for h in headers]
    widths = [max(len(str(c)) for c in col) for col in cols]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print(fmt.format(*[str(c) for c in r]))
```

#### Commit 4 — `ui: add menu() — numbered menu, returns chosen index`

**File:** `ui/console.py`

```python
def menu(title, options):
    print(f"\n=== {title} ===")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        raw = input("> ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw) - 1
        print(f"  enter 1..{len(options)}.")
```

#### Commit 5 — `main: hook menu into "Add student" action`

**File:** `main.py`

Member 2 has set up the action dispatch. You add or refine the `action_add_student` function to use `prompt` and `prompt_int`, and confirm duplicate student IDs are rejected.

#### Commit 6 — `main: hook menu into "List students" + "Add grade" actions`

**File:** `main.py`

Wire `action_list_students` to use your `print_table`. Wire `action_add_grade` to use `prompt_int` (student id), `prompt` (course code), `prompt_float` (score), and report errors clearly when the student doesn't exist.

#### Commit 7 — `main: hook menu into reports + save/load actions`

**File:** `main.py`

Wire `action_top_students`, `action_failing`, `action_averages`, `action_save` — each uses `print_table` for output.

#### Commit 8 — `docs: README run instructions + sample output`

**File:** `README.md`

Polish the README so a grader can run the project in 30 seconds:

```markdown
# Student Grade Management System

Console application (Python 3.10+) that manages students, courses, and grades.
Built as the ITP2 final project, AITU, Spring 2026.

## Features
- Add students and courses
- Assign grades
- Calculate credit-weighted GPA on the 4.0 scale
- Reports: top N students, failing students, course averages
- Load/save data from CSV and JSON

## How to run
```powershell
python main.py
```
Default admin credentials (demo only): username `admin` / password `admin`.

## How to run tests
```powershell
python -m unittest discover tests
```

## Team
| Member        | Area                          | GitHub |
|---------------|-------------------------------|--------|
| <Name 1>      | Services (GPA, reports)       | @...   |
| <Name 2>      | Models, integration           | @...   |
| <Name 3>      | File I/O, validators          | @...   |
| <Name 4>      | Console UI, docs              | @...   |

## Sample output
(paste a screenshot of `python main.py` running here)
```

---

## Phase 3 — Coordination rules (everyone follows)

### Order of work (so nobody blocks)

```
Week 1:   Member 2 (models)  ──► merged first; everyone else needs these classes
Week 2:   Member 1 (services) and Member 3 (utils) work in parallel
Week 3:   Member 4 (UI/docs) finalises; everyone reviews & writes tests
```

If your area depends on someone else's, write your tests against the **expected interface** (defined in this doc) and merge them ahead of the implementation. Then your code goes green when their PR merges.

### Pull request rules

- One PR per branch. Title matches your branch (`feat/services` → "Services").
- At least one other teammate **must review** before merge.
- Squash-merging is **forbidden** — it would collapse your 8 commits into 1. Use **"Create a merge commit"** in GitHub.

### Daily routine

1. `git checkout main && git pull` — get the latest from teammates.
2. `git checkout feat/<area>` — back to your branch.
3. `git merge main` — pull their changes into yours.
4. Work, commit, push.

### Before the final submission (everyone, last day)

1. Run all tests on `main`: `python -m unittest discover tests` — must pass.
2. Run the app: `python main.py` — try every menu option.
3. Check `git log --oneline | wc -l` — should be ~32 commits.
4. Check `git shortlog -sn` — should show 4 names with similar counts.
5. Build the presentation (5–10 slides, see section 5.2 of the requirements PDF).
6. Each person **rehearses** explaining their own module — that's the code defence.

### What each person says in the code defence

| Member | Talking points |
|---|---|
| 1 | "I used a generator (`gpa_for_all`) instead of building a full list — saves memory for large rosters. Decorators (`@log_call`, `@timed`) add observability without modifying the core logic. Sorting with `lambda` and filtering with `filter()` are clean and idiomatic." |
| 2 | "OOP: `Person` is the base with encapsulated `_id`/`_name`. `Student` and `Admin` inherit and override `role()` — polymorphism. `Course.__eq__` and `__hash__` let us use Course in sets. `Grade.LETTER_BOUNDS` is a tuple because it's a constant lookup table." |
| 3 | "CSV with `DictReader` for clean row access. Dict keyed by student id gives O(1) lookups vs O(n) for a list. Regex validators (`re.compile`) catch malformed input at the boundary. Roundtrip test ensures save/load are inverses." |
| 4 | "Menu loop with retry-on-bad-input — no crashes from typos. `print_table` aligns columns dynamically. The UI module imports nothing from `services` or `models`, so it stays independently testable." |
