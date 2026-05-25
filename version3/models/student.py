"""Student model — concrete subclass of :class:`Person`."""
from __future__ import annotations

from dataclasses import dataclass

from models.person import Person


@dataclass
class Student(Person):
    """A learner enrolled in zero or more courses.

    Inherits ``id``, ``first_name``, ``last_name`` from :class:`Person`
    and overrides :meth:`role` (polymorphism).
    """

    email: str = ""

    def role(self) -> str:
        return "Student"

    def to_row(self) -> tuple[int | None, str, str, str]:
        """Return a tuple suitable for SQLite parameter binding."""
        return (self.id, self.first_name, self.last_name, self.email)

    @classmethod
    def from_row(cls, row: tuple) -> "Student":
        """Construct from a SQLite row ``(id, first_name, last_name, email)``."""
        sid, first, last, email = row
        return cls(id=sid, first_name=first, last_name=last, email=email or "")
