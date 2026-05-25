"""CRUD + analytics for students."""
from __future__ import annotations

from typing import Iterator

from database import Database
from models.student import Student
from models.course import Course
from models.enrollment import Enrollment
from utils.gpa import cumulative_gpa


class StudentService:
    """Operations on the ``students`` table and related joins."""

    def __init__(self, db: Database) -> None:
        self.db = db

    # ---------- create / read / update / delete ----------------------------

    def create(self, first: str, last: str, email: str = "") -> Student:
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO students (first_name, last_name, email) VALUES (?, ?, ?)",
                (first, last, email),
            )
            return Student(id=cur.lastrowid, first_name=first, last_name=last, email=email)

    def get(self, student_id: int) -> Student | None:
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT id, first_name, last_name, email FROM students WHERE id = ?",
                (student_id,),
            )
            row = cur.fetchone()
            return Student.from_row(row) if row else None

    def all(self) -> list[Student]:
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT id, first_name, last_name, email FROM students ORDER BY id"
            )
            return [Student.from_row(r) for r in cur.fetchall()]

    def iter_all(self) -> Iterator[Student]:
        """Yield students one-by-one (generator — useful for large datasets)."""
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT id, first_name, last_name, email FROM students ORDER BY id"
            )
            for row in cur:
                yield Student.from_row(row)

    def update(self, student_id: int, first: str, last: str, email: str) -> None:
        with self.db.cursor() as cur:
            cur.execute(
                "UPDATE students SET first_name=?, last_name=?, email=? WHERE id=?",
                (first, last, email, student_id),
            )
            if cur.rowcount == 0:
                raise KeyError(f"student #{student_id} not found")

    def delete(self, student_id: int) -> None:
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
            if cur.rowcount == 0:
                raise KeyError(f"student #{student_id} not found")

    # ---------- analytics --------------------------------------------------

    def grade_count(self, student_id: int) -> int:
        """Number of trimester scores recorded for the student."""
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT
                    (CASE WHEN t1 IS NOT NULL THEN 1 ELSE 0 END) +
                    (CASE WHEN t2 IS NOT NULL THEN 1 ELSE 0 END) +
                    (CASE WHEN t3 IS NOT NULL THEN 1 ELSE 0 END)
                FROM enrollments WHERE student_id = ?
                """,
                (student_id,),
            )
            return sum(row[0] for row in cur.fetchall())

    def course_count(self, student_id: int) -> int:
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM enrollments WHERE student_id = ?", (student_id,)
            )
            return int(cur.fetchone()[0])

    def enrollments_with_courses(
        self, student_id: int
    ) -> list[tuple[Enrollment, Course]]:
        """Return every (enrollment, course) pair for the student."""
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT e.id, e.student_id, e.course_id, e.t1, e.t2, e.t3,
                       c.id, c.name, c.credits, c.hours
                FROM enrollments e
                JOIN courses    c ON c.id = e.course_id
                WHERE e.student_id = ?
                ORDER BY c.name
                """,
                (student_id,),
            )
            return [
                (
                    Enrollment.from_row(row[:6]),
                    Course.from_row(row[6:]),
                )
                for row in cur.fetchall()
            ]

    def cgpa(self, student_id: int) -> float | None:
        """Cumulative GPA across all the student's courses (credit-weighted)."""
        pairs = self.enrollments_with_courses(student_id)
        return cumulative_gpa(
            (enr.final_score, course.credits) for enr, course in pairs
        )
