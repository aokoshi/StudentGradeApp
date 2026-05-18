# Per-member task & commit plan

Goal: **each member ~8 commits** (32 total) so commit history looks balanced.
The 2 stronger members do harder algorithmic / OOP work in fewer-but-bigger commits;
the 2 less-experienced members do straightforward file-I/O and console work, sliced
into many small commits.

> Make each commit on your **own machine** so your name appears in `git log`.
> Suggested git workflow:
>
> ```bash
> git checkout -b feat/<your-area>     # one branch per member
> # ... edit, test, commit ...
> git push origin feat/<your-area>
> # open a Pull Request → merge into main
> ```

---

## Member 1 — Services (HARD)

Owns: `services/gpa_calculator.py`, `services/report_generator.py`, `services/decorators.py`, `tests/test_services.py`

1. `services: scaffold package with __init__.py exports`
2. `services: add @log_call decorator`
3. `services: add @timed decorator using time.perf_counter`
4. `services: implement basic calculate_gpa (credit-weighted, 4.0 scale)`
5. `services: extract gpa_for_all as generator for lazy evaluation`
6. `services: add top_students using sorted + lambda key`
7. `services: add failing_students (filter) and course_averages`
8. `tests: cover GPA edge cases, top-N order, course averages`

## Member 2 — Models & integration (HARD)

Owns: `models/*.py`, `main.py`, `tests/test_models.py`

1. `models: add Person base class with encapsulated id/name`
2. `models: add Student subclass with grades list and courses set`
3. `models: add Admin subclass with verify(username, password)`
4. `models: add Course with __eq__ / __hash__ on code`
5. `models: add Grade with letter/GPA mapping (LETTER_BOUNDS tuple)`
6. `models: re-export everything from __init__.py`
7. `main: wire models + services + utils into console menu loop`
8. `tests: cover model construction, polymorphism, validation`

## Member 3 — Utils & data (EASY)

Owns: `utils/*.py`, `data/*`, `tests/test_utils.py`

1. `data: add sample grades.csv (8 rows, 4 students, 3 courses)`
2. `data: add courses.json course catalog`
3. `utils: implement load_grades_csv (DictReader → Student + Grade objects)`
4. `utils: implement save_grades_csv (DictWriter)`
5. `utils: implement load_json / save_json helpers`
6. `utils: regex validators for email, score range, course code`
7. `tests: csv roundtrip (save → load → assert equality)`
8. `tests: validators (valid + invalid inputs)`

## Member 4 — Console UI (EASY)

Owns: `ui/console.py`, parts of `main.py` menu, `README.md` final pass

1. `ui: scaffold console.py with prompt() helper`
2. `ui: add prompt_int + prompt_float with retry-on-bad-input`
3. `ui: add print_table — minimal pretty 2D table printer`
4. `ui: add menu() — numbered menu, returns chosen index`
5. `main: hook menu into "Add student" action`
6. `main: hook menu into "List students" + "Add grade" actions`
7. `main: hook menu into reports + save/load actions`
8. `docs: README run instructions + sample output screenshot`

---

## Coordination tips

- Pull `main` daily before starting work so you don't drift.
- The strong members' modules (`models`, `services`) have **no UI imports** — keep that boundary so everyone can develop independently.
- If your area is blocked waiting on another member, write tests against the *expected* interface (defined here in TASKS.md) and merge them ahead of the implementation.
- Final week: everyone reviews everyone else's tests, prepares slides, and rehearses the individual defense (each person explains their own module).
