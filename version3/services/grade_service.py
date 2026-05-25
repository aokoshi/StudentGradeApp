"""Enrollment + grade entry logic."""
from __future__ import annotations

from database import Database
from models.enrollment import Enrollment


class GradeService:
    """Manage the ``enrollments`` table (the join between students/courses)."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def enroll(self, student_id: int, course_id: int) -> Enrollment:
        """Create an enrollment row; raises if one already exists."""
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
                (student_id, course_id),
            )
            return Enrollment(id=cur.lastrowid, student_id=student_id, course_id=course_id)

    def unenroll(self, student_id: int, course_id: int) -> None:
        with self.db.cursor() as cur:
            cur.execute(
                "DELETE FROM enrollments WHERE student_id=? AND course_id=?",
                (student_id, course_id),
            )
            if cur.rowcount == 0:
                raise KeyError("enrollment does not exist")

    def get(self, student_id: int, course_id: int) -> Enrollment | None:
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT id, student_id, course_id, t1, t2, t3 "
                "FROM enrollments WHERE student_id=? AND course_id=?",
                (student_id, course_id),
            )
            row = cur.fetchone()
            return Enrollment.from_row(row) if row else None

    def set_trimester_score(
        self, student_id: int, course_id: int, trimester: int, score: float
    ) -> None:
        """Update a single trimester score (1, 2, or 3) for an enrollment."""
        if trimester not in (1, 2, 3):
            raise ValueError("trimester must be 1, 2, or 3")
        column = f"t{trimester}"
        with self.db.cursor() as cur:
            cur.execute(
                f"UPDATE enrollments SET {column}=? WHERE student_id=? AND course_id=?",
                (score, student_id, course_id),
            )
            if cur.rowcount == 0:
                raise KeyError(
                    f"student #{student_id} is not enrolled in course #{course_id}"
                )
