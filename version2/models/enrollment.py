"""Course model."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Course:
    """A course offered to students.

    Attributes
    ----------
    id:
        Database primary key, ``None`` for an unsaved instance.
    name:
        Human-readable course title (e.g. ``"Intro to Programming 2"``).
    credits:
        Credit weight used in cGPA calculation.
    hours:
        Total contact / lecture hours for the course.
    """

    id: int | None
    name: str
    credits: int
    hours: int

    def to_row(self) -> tuple[int | None, str, int, int]:
        return (self.id, self.name, self.credits, self.hours)

    @classmethod
    def from_row(cls, row: tuple) -> "Course":
        cid, name, credits_, hours = row
        return cls(id=cid, name=name, credits=int(credits_), hours=int(hours))
