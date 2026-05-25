"""Menu loops — orchestrate the user-facing flow.

Each ``_menu_*`` function pushes a new breadcrumb level and runs its own
loop until the user picks "Back". The top-level :func:`run_main_menu`
is the only public entry point.
"""
from __future__ import annotations

import sqlite3

from services       import CourseService, GradeService, StudentService
from ui.console     import ConsoleUI
from ui.views       import (
    render_course_details,
    render_courses_table,
    render_student_courses_for_grading,
    render_student_profile,
    render_students_table,
)
from utils.decorators import catch_errors, confirm_action
from utils.validators import (
    is_valid_email,
    is_valid_name,
    parse_int,
    parse_score,
)


# =========================================================================
# Main menu
# =========================================================================

def run_main_menu(
    ui: ConsoleUI,
    students: StudentService,
    courses: CourseService,
    grades: GradeService,
) -> None:
    """Top-level loop. Returns when the user chooses "Exit"."""
    crumbs = ["Home"]
    while True:
        ui.clear()
        ui.banner(crumbs)
        ui.console.print(
            "[bold]1.[/bold] Manage Students\n"
            "[bold]2.[/bold] Manage Courses\n"
            "[bold]3.[/bold] Add / Update Grades\n"
            "[bold]4.[/bold] Reports\n"
            "[bold]0.[/bold] Exit"
        )
        choice = ui.ask_choice("Select an option", ["0", "1", "2", "3", "4"])
        if   choice == "1": _menu_students(ui, students, courses, grades)
        elif choice == "2": _menu_courses(ui, students, courses, grades)
        elif choice == "3": _grading_workflow(ui, students, courses, grades)
        elif choice == "4": _menu_reports(ui, students, courses)
        elif choice == "0":
            ui.console.print("[cyan]Goodbye![/cyan]")
            return


# =========================================================================
# Students
# =========================================================================

def _menu_students(
    ui: ConsoleUI,
    students: StudentService,
    courses: CourseService,
    grades: GradeService,
) -> None:
    crumbs = ["Home", "Students"]
    while True:
        ui.clear()
        ui.banner(crumbs)
        render_students_table(ui.console, students.all(), students)
        ui.console.print(
            "\n[bold]1.[/bold] Add Student\n"
            "[bold]2.[/bold] View Student Details\n"
            "[bold]3.[/bold] Update Student\n"
            "[bold]4.[/bold] Delete Student\n"
            "[bold]5.[/bold] Enroll Student in Course\n"
            "[bold]0.[/bold] Back"
        )
        choice = ui.ask_choice("Select an option", ["0", "1", "2", "3", "4", "5"])
        if   choice == "1": _action_add_student(ui, students)
        elif choice == "2": _action_view_student(ui, students)
        elif choice == "3": _action_update_student(ui, students)
        elif choice == "4": _action_delete_student(ui, students)
        elif choice == "5": _action_enroll_student(ui, students, courses, grades)
        elif choice == "0": return


@catch_errors
def _action_add_student(ui: ConsoleUI, students: StudentService) -> None:
    first = ui.ask("First name").strip()
    last  = ui.ask("Last name").strip()
    email = ui.ask("Email (optional)", default="").strip()
    if not is_valid_name(first) or not is_valid_name(last):
        raise ValueError("names must contain only letters, spaces, '-' or '''")
    if email and not is_valid_email(email):
        raise ValueError("invalid email format")
    s = students.create(first, last, email)
    ui.success(f"Student #{s.id} ({s.full_name}) created.")
    ui.pause()


@catch_errors
def _action_view_student(ui: ConsoleUI, students: StudentService) -> None:
    sid = parse_int(ui.ask("Student ID"), minimum=1)
    s = students.get(sid)
    if not s:
        raise KeyError(f"student #{sid} not found")
    ui.clear()
    ui.banner(["Home", "Students", "Details"])
    render_student_profile(ui.console, s, students)
    ui.pause()


@catch_errors
def _action_update_student(ui: ConsoleUI, students: StudentService) -> None:
    sid = parse_int(ui.ask("Student ID to update"), minimum=1)
    current = students.get(sid)
    if not current:
        raise KeyError(f"student #{sid} not found")
    first = ui.ask("First name", default=current.first_name).strip()
    last  = ui.ask("Last name",  default=current.last_name).strip()
    email = ui.ask("Email",      default=current.email or "").strip()
    if not is_valid_name(first) or not is_valid_name(last):
        raise ValueError("invalid name")
    if email and not is_valid_email(email):
        raise ValueError("invalid email format")
    students.update(sid, first, last, email)
    ui.success(f"Student #{sid} updated.")
    ui.pause()


@catch_errors
def _action_delete_student(ui: ConsoleUI, students: StudentService) -> None:
    sid = parse_int(ui.ask("Student ID to delete"), minimum=1)
    if not students.get(sid):
        raise KeyError(f"student #{sid} not found")

    @confirm_action(f"Permanently delete student #{sid} and all their grades?")
    def _do() -> None:
        students.delete(sid)
        ui.success(f"Student #{sid} deleted.")

    _do()
    ui.pause()


@catch_errors
def _action_enroll_student(
    ui: ConsoleUI,
    students: StudentService,
    courses: CourseService,
    grades: GradeService,
) -> None:
    sid = parse_int(ui.ask("Student ID"), minimum=1)
    if not students.get(sid):
        raise KeyError(f"student #{sid} not found")
    render_courses_table(ui.console, courses.all(), courses)
    cid = parse_int(ui.ask("Course ID to enroll in"), minimum=1)
    if not courses.get(cid):
        raise KeyError(f"course #{cid} not found")
    try:
        grades.enroll(sid, cid)
    except sqlite3.IntegrityError:
        raise ValueError("student is already enrolled in that course")
    ui.success(f"Student #{sid} enrolled in course #{cid}.")
    ui.pause()


# =========================================================================
# Courses
# =========================================================================

def _menu_courses(
    ui: ConsoleUI,
    students: StudentService,
    courses: CourseService,
    grades: GradeService,
) -> None:
    crumbs = ["Home", "Courses"]
    while True:
        ui.clear()
        ui.banner(crumbs)
        render_courses_table(ui.console, courses.all(), courses)
        ui.console.print(
            "\n[bold]1.[/bold] Add Course\n"
            "[bold]2.[/bold] View Course Details\n"
            "[bold]3.[/bold] Update Course\n"
            "[bold]4.[/bold] Delete Course\n"
            "[bold]0.[/bold] Back"
        )
        choice = ui.ask_choice("Select an option", ["0", "1", "2", "3", "4"])
        if   choice == "1": _action_add_course(ui, courses)
        elif choice == "2": _action_view_course(ui, courses)
        elif choice == "3": _action_update_course(ui, courses)
        elif choice == "4": _action_delete_course(ui, courses)
        elif choice == "0": return


@catch_errors
def _action_add_course(ui: ConsoleUI, courses: CourseService) -> None:
    name    = ui.ask("Course name").strip()
    credits = parse_int(ui.ask("Credits"), minimum=1, maximum=10)
    hours   = parse_int(ui.ask("Hours"),   minimum=1, maximum=500)
    if not name:
        raise ValueError("course name cannot be empty")
    try:
        c = courses.create(name, credits, hours)
    except sqlite3.IntegrityError:
        raise ValueError(f"a course named {name!r} already exists")
    ui.success(f"Course #{c.id} ({c.name}) created.")
    ui.pause()


@catch_errors
def _action_view_course(ui: ConsoleUI, courses: CourseService) -> None:
    cid = parse_int(ui.ask("Course ID"), minimum=1)
    c = courses.get(cid)
    if not c:
        raise KeyError(f"course #{cid} not found")
    ui.clear()
    ui.banner(["Home", "Courses", "Details"])
    render_course_details(ui.console, c, courses)
    ui.pause()


@catch_errors
def _action_update_course(ui: ConsoleUI, courses: CourseService) -> None:
    cid = parse_int(ui.ask("Course ID"), minimum=1)
    current = courses.get(cid)
    if not current:
        raise KeyError(f"course #{cid} not found")
    name    = ui.ask("Name",    default=current.name).strip()
    credits = parse_int(ui.ask("Credits", default=str(current.credits)), minimum=1, maximum=10)
    hours   = parse_int(ui.ask("Hours",   default=str(current.hours)),   minimum=1, maximum=500)
    courses.update(cid, name, credits, hours)
    ui.success(f"Course #{cid} updated.")
    ui.pause()


@catch_errors
def _action_delete_course(ui: ConsoleUI, courses: CourseService) -> None:
    cid = parse_int(ui.ask("Course ID"), minimum=1)
    if not courses.get(cid):
        raise KeyError(f"course #{cid} not found")

    @confirm_action(f"Delete course #{cid} and all enrollments in it?")
    def _do() -> None:
        courses.delete(cid)
        ui.success(f"Course #{cid} deleted.")

    _do()
    ui.pause()


# =========================================================================
# Grading workflow
# =========================================================================

@catch_errors
def _grading_workflow(
    ui: ConsoleUI,
    students: StudentService,
    courses: CourseService,
    grades: GradeService,
) -> None:
    """Implements the required flow: list students → pick → list THEIR courses → pick → set score."""
    ui.clear()
    ui.banner(["Home", "Grades"])
    render_students_table(ui.console, students.all(), students)
    sid = parse_int(ui.ask("\nStudent ID"), minimum=1)
    if not students.get(sid):
        raise KeyError(f"student #{sid} not found")

    pairs = students.enrollments_with_courses(sid)
    if not pairs:
        raise ValueError(
            "this student is not enrolled in any course — enroll them first"
        )

    ui.console.print()
    render_student_courses_for_grading(ui.console, pairs)
    valid_course_ids = {course.id for _enr, course in pairs}

    cid = parse_int(ui.ask("\nCourse ID (from the table above)"), minimum=1)
    if cid not in valid_course_ids:
        raise ValueError("that course is not in this student's enrollments")

    trimester = parse_int(ui.ask("Trimester (1/2/3)"), minimum=1, maximum=3)
    score     = parse_score(ui.ask("Score (0–100)"))
    grades.set_trimester_score(sid, cid, trimester, score)
    ui.success(
        f"Recorded T{trimester} = {score:.1f} for student #{sid} in course #{cid}."
    )
    ui.pause()


# =========================================================================
# Reports
# =========================================================================

def _menu_reports(
    ui: ConsoleUI,
    students: StudentService,
    courses: CourseService,
) -> None:
    crumbs = ["Home", "Reports"]
    while True:
        ui.clear()
        ui.banner(crumbs)
        ui.console.print(
            "[bold]1.[/bold] Top students by cGPA\n"
            "[bold]2.[/bold] Full student listing\n"
            "[bold]3.[/bold] Full course listing\n"
            "[bold]0.[/bold] Back"
        )
        choice = ui.ask_choice("Select an option", ["0", "1", "2", "3"])
        if   choice == "1": _report_top_students(ui, students)
        elif choice == "2":
            render_students_table(ui.console, students.all(), students)
            ui.pause()
        elif choice == "3":
            render_courses_table(ui.console, courses.all(), courses)
            ui.pause()
        elif choice == "0": return


@catch_errors
def _report_top_students(ui: ConsoleUI, students: StudentService) -> None:
    """List top-N students by cGPA (lambda used for sorting key)."""
    n = parse_int(ui.ask("How many to show?", default="5"), minimum=1, maximum=100)
    all_students  = students.all()
    with_gpa      = [(s, students.cgpa(s.id)) for s in all_students]
    graded        = list(filter(lambda pair: pair[1] is not None, with_gpa))
    graded.sort(key=lambda pair: pair[1], reverse=True)
    from rich.table import Table
    table = Table(title=f"Top {min(n, len(graded))} Students by cGPA", header_style="bold yellow")
    table.add_column("Rank", justify="right", style="dim")
    table.add_column("ID",   justify="right")
    table.add_column("Full Name")
    table.add_column("cGPA", justify="right", style="bold")
    for rank, (s, gpa) in enumerate(graded[:n], start=1):
        table.add_row(str(rank), str(s.id), s.full_name, f"{gpa:.2f}")
    if not graded:
        ui.console.print("[yellow]No graded students to rank yet.[/yellow]")
    else:
        ui.console.print(table)
    ui.pause()
