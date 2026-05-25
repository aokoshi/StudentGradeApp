"""CRUD + analytics for courses."""
from __future__ import annotations

from database import Database
from models.course import Course
from models.enrollment import Enrollment
from models.student import Student


class CourseService:
    """Operations on the ``courses`` table and related joins."""

    def __init__(self, db: Database) -> None:
        self.db = db

    # ---------- CRUD --------------------------------------------------------

    def create(self, name: str, credits: int, hours: int) -> Course:
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO courses (name, credits, hours) VALUES (?, ?, ?)",
                (name, credits, hours),
            )
            return Course(id=cur.lastrowid, name=name, credits=credits, hours=hours)

    def get(self, course_id: int) -> Course | None:
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT id, name, credits, hours FROM courses WHERE id = ?",
                (course_id,),
            )
            row = cur.fetchone()
            return Course.from_row(row) if row else None

    def all(self) -> list[Course]:
        with self.db.cursor() as cur:
            cur.execute("SELECT id, name, credits, hours FROM courses ORDER BY id")
            return [Course.from_row(r) for r in cur.fetchall()]

    def update(self, course_id: int, name: str, credits: int, hours: int) -> None:
        with self.db.cursor() as cur:
            cur.execute(
                "UPDATE courses SET name=?, credits=?, hours=? WHERE id=?",
                (name, credits, hours, course_id),
            )
            if cur.rowcount == 0:
                raise KeyError(f"course #{course_id} not found")

    def delete(self, course_id: int) -> None:
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM courses WHERE id = ?", (course_id,))
            if cur.rowcount == 0:
                raise KeyError(f"course #{course_id} not found")

    # ---------- analytics --------------------------------------------------

    def student_count(self, course_id: int) -> int:
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM enrollments WHERE course_id = ?", (course_id,)
            )
            return int(cur.fetchone()[0])

    def enrolled_students(
        self, course_id: int
    ) -> list[tuple[Student, Enrollment]]:
        """Every student in the course paired with their enrollment row."""
        with self.db.cursor() as cur:
            cur.execute(
                """
                SELECT s.id, s.first_name, s.last_name, s.email,
                       e.id, e.student_id, e.course_id, e.t1, e.t2, e.t3
                FROM enrollments e
                JOIN students    s ON s.id = e.student_id
                WHERE e.course_id = ?
                ORDER BY s.last_name, s.first_name
                """,
                (course_id,),
            )
            return [
                (Student.from_row(row[:4]), Enrollment.from_row(row[4:]))
                for row in cur.fetchall()
            ]
