"""Abstract base class for any person in the system."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Person(ABC):
    """Abstract base providing identity and naming behavior.

    Demonstrates encapsulation (private-ish id), inheritance (Student
    extends Person) and polymorphism (subclasses override ``role``).
    """

    id: int | None
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @abstractmethod
    def role(self) -> str:
        """Return a human-readable role label."""
