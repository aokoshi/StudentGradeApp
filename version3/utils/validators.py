"""Input validation helpers — pure functions, easy to unit-test."""
from __future__ import annotations

import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
NAME_RE  = re.compile(r"^[A-Za-z][A-Za-z'\- ]{0,49}$")


def is_valid_email(value: str) -> bool:
    """Return True if *value* looks like an email address."""
    return bool(EMAIL_RE.match(value.strip()))


def is_valid_name(value: str) -> bool:
    """Return True if *value* is a plausible first or last name."""
    return bool(NAME_RE.match(value.strip()))


def parse_int(value: str, *, minimum: int | None = None, maximum: int | None = None) -> int:
    """Parse *value* as int with optional bounds; raises ``ValueError`` on failure."""
    n = int(value.strip())
    if minimum is not None and n < minimum:
        raise ValueError(f"value must be >= {minimum}")
    if maximum is not None and n > maximum:
        raise ValueError(f"value must be <= {maximum}")
    return n


def parse_score(value: str) -> float:
    """Parse a 0–100 score (allows decimals like ``87.5``)."""
    s = float(value.strip())
    if not 0 <= s <= 100:
        raise ValueError("score must be between 0 and 100")
    return s
