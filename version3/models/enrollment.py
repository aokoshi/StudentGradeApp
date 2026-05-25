"""Enrollment links a student to a course and stores trimester scores."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Enrollment:
    """A student's participation in a single course.

    Scores are stored on a 0–100 scale and may be ``None`` if not yet
    entered. The final course score is the simple mean of the three
    trimesters that have been recorded.
    """

    id: int | None
    student_id: int
    course_id: int
    t1: float | None = None
    t2: float | None = None
    t3: float | None = None

    @property
    def recorded_scores(self) -> list[float]:
        """Return the list of non-``None`` trimester scores."""
        return [s for s in (self.t1, self.t2, self.t3) if s is not None]

    @property
    def final_score(self) -> float | None:
        """Average of recorded trimester scores, or ``None`` if none recorded."""
        scores = self.recorded_scores
        if not scores:
            return None
        return sum(scores) / len(scores)

    def to_row(self) -> tuple:
        return (
            self.id,
            self.student_id,
            self.course_id,
            self.t1,
            self.t2,
            self.t3,
        )

    @classmethod
    def from_row(cls, row: tuple) -> "Enrollment":
        eid, sid, cid, t1, t2, t3 = row
        return cls(id=eid, student_id=sid, course_id=cid, t1=t1, t2=t2, t3=t3)
