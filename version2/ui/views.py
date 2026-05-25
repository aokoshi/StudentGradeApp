"""View functions — render tables and detail panels using rich."""
from __future__ import annotations

from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table

from models.course     import Course
from models.enrollment import Enrollment
from models.student    import Student
from services          import CourseService, StudentService
from utils.gpa         import score_to_gpa, score_to_letter


def _format_gpa(value: float | None) -> str:
    return f"{value:.2f}" if value is not None else "-"


def _format_score(value: float | None) -> str:
    return f"{value:.1f}" if value is not None else "-"


# ---------- student tables / profiles ------------------------------------

def render_students_table(
    console: Console,
    students: list[Student],
    student_service: StudentService,
) -> None:
    """Comprehensive student listing — ID, Name, Grades, Courses, cGPA."""
    table = Table(title="All Students", header_style="bold cyan", expand=True)
    table.add_column("ID",      justify="right", style="dim")
    table.add_column("Full Name")
    table.add_column("Grades",  justify="right")
    table.add_column("Courses", justify="right")
    table.add_column("cGPA",    justify="right", style="bold")

    if not students:
        console.print("[yellow]No students yet — add one from the menu.[/yellow]")
        return

    for s in students:
        table.add_row(
            str(s.id),
            s.full_name,
            str(student_service.grade_count(s.id)),
            str(student_service.course_count(s.id)),
            _format_gpa(student_service.cgpa(s.id)),
        )
    console.print(table)


def render_student_profile(
    console: Console,
    student: Student,
    student_service: StudentService,
) -> None:
    """Detail view for a single student — info + per-course breakdown."""
    cgpa = student_service.cgpa(student.id)

    info = (
        f"[bold]ID:[/bold] {student.id}\n"
        f"[bold]Name:[/bold] {student.full_name}\n"
        f"[bold]Email:[/bold] {student.email or '-'}\n"
        f"[bold]cGPA:[/bold] {_format_gpa(cgpa)} / 4.00"
    )
    console.print(Panel(info, title="Student Profile", border_style="green"))

    pairs = student_service.enrollments_with_courses(student.id)
    if not pairs:
        console.print("[dim]This student is not enrolled in any courses yet.[/dim]")
        return

    table = Table(title="Enrolled Courses", header_style="bold magenta")
    table.add_column("Course ID", justify="right", style="dim")
    table.add_column("Course Name")
    table.add_column("Credits", justify="right")
    table.add_column("T1", justify="right")
    table.add_column("T2", justify="right")
    table.add_column("T3", justify="right")
    table.add_column("Final %", justify="right")
    table.add_column("Letter", justify="center")
    table.add_column("GPA", justify="right", style="bold")

    for enrollment, course in pairs:
        table.add_row(
            str(course.id),
            course.name,
            str(course.credits),
            _format_score(enrollment.t1),
            _format_score(enrollment.t2),
            _format_score(enrollment.t3),
            _format_score(enrollment.final_score),
            score_to_letter(enrollment.final_score),
            _format_gpa(score_to_gpa(enrollment.final_score)),
        )
    console.print(table)


# ---------- course tables / details --------------------------------------

def render_courses_table(
    console: Console,
    courses: list[Course],
    course_service: CourseService,
) -> None:
    table = Table(title="All Courses", header_style="bold cyan", expand=True)
    table.add_column("ID",       justify="right", style="dim")
    table.add_column("Name")
    table.add_column("Credits",  justify="right")
    table.add_column("Hours",    justify="right")
    table.add_column("Students", justify="right", style="bold")

    if not courses:
        console.print("[yellow]No courses yet — add one from the menu.[/yellow]")
        return

    for c in courses:
        table.add_row(
            str(c.id),
            c.name,
            str(c.credits),
            str(c.hours),
            str(course_service.student_count(c.id)),
        )
    console.print(table)


def render_course_details(
    console: Console,
    course: Course,
    course_service: CourseService,
) -> None:
    info = (
        f"[bold]Course ID:[/bold] {course.id}\n"
        f"[bold]Name:[/bold] {course.name}\n"
        f"[bold]Credits:[/bold] {course.credits}\n"
        f"[bold]Hours:[/bold] {course.hours}"
    )
    console.print(Panel(info, title="Course Details", border_style="green"))

    rows = course_service.enrolled_students(course.id)
    if not rows:
        console.print("[dim]No students enrolled in this course yet.[/dim]")
        return

    table = Table(title="Enrolled Students", header_style="bold magenta")
    table.add_column("Student ID", justify="right", style="dim")
    table.add_column("Full Name")
    table.add_column("T1 GPA",     justify="right")
    table.add_column("T2 GPA",     justify="right")
    table.add_column("T3 GPA",     justify="right")
    table.add_column("Final %",    justify="right")
    table.add_column("Course GPA", justify="right", style="bold")

    for student, enr in rows:
        table.add_row(
            str(student.id),
            student.full_name,
            _format_gpa(score_to_gpa(enr.t1)),
            _format_gpa(score_to_gpa(enr.t2)),
            _format_gpa(score_to_gpa(enr.t3)),
            _format_score(enr.final_score),
            _format_gpa(score_to_gpa(enr.final_score)),
        )
    console.print(table)


# ---------- helper for grading workflow ----------------------------------

def render_student_courses_for_grading(
    console: Console,
    pairs: list[tuple[Enrollment, Course]],
) -> None:
    """Show only the courses a specific student is enrolled in."""
    table = Table(
        title="Courses for this student",
        header_style="bold cyan",
    )
    table.add_column("Course ID", justify="right", style="dim")
    table.add_column("Name")
    table.add_column("Credits", justify="right")
    table.add_column("T1", justify="right")
    table.add_column("T2", justify="right")
    table.add_column("T3", justify="right")

    for enr, course in pairs:
        table.add_row(
            str(course.id),
            course.name,
            str(course.credits),
            _format_score(enr.t1),
            _format_score(enr.t2),
            _format_score(enr.t3),
        )
    console.print(table)
