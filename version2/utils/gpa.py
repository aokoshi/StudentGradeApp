"""GPA conversion + cumulative GPA math.

Uses the standard AITU 100-point → 4.0 letter scale:

    95–100 : A   4.00
    90–94  : A-  3.67
    85–89  : B+  3.33
    80–84  : B   3.00
    75–79  : B-  2.67
    70–74  : C+  2.33
    65–69  : C   2.00
    60–64  : C-  1.67
    55–59  : D+  1.33
    50–54  : D   1.00
    < 50   : F   0.00
"""
from __future__ import annotations

from typing import Iterable

# (lower_inclusive, letter, gpa_points). Sorted high→low for short-circuit lookup.
GRADE_TABLE: tuple[tuple[int, str, float], ...] = (
    (95, "A",  4.00),
    (90, "A-", 3.67),
    (85, "B+", 3.33),
    (80, "B",  3.00),
    (75, "B-", 2.67),
    (70, "C+", 2.33),
    (65, "C",  2.00),
    (60, "C-", 1.67),
    (55, "D+", 1.33),
    (50, "D",  1.00),
    (0,  "F",  0.00),
)


def score_to_gpa(score: float | None) -> float | None:
    """Convert a 0–100 score to a 4.0 GPA point value.

    Returns ``None`` when the score is missing so callers can distinguish
    "not graded yet" from "graded zero".
    """
    if score is None:
        return None
    if not 0 <= score <= 100:
        raise ValueError(f"score must be in [0, 100], got {score!r}")
    # First entry whose lower bound is <= score wins.
    return next(points for lower, _letter, points in GRADE_TABLE if score >= lower)


def score_to_letter(score: float | None) -> str:
    """Convert a 0–100 score to a letter grade (``"-"`` when missing)."""
    if score is None:
        return "-"
    return next(letter for lower, letter, _pts in GRADE_TABLE if score >= lower)


def cumulative_gpa(course_results: Iterable[tuple[float | None, int]]) -> float | None:
    """Compute credit-weighted cGPA.

    Parameters
    ----------
    course_results:
        Iterable of ``(final_score, credits)`` tuples — one per course the
        student is enrolled in. Courses without a final score are skipped.

    Returns
    -------
    Weighted GPA on a 0.00–4.00 scale, or ``None`` if no graded courses.
    """
    total_points = 0.0
    total_credits = 0
    for score, credits in course_results:
        gpa = score_to_gpa(score)
        if gpa is None:
            continue
        total_points  += gpa * credits
        total_credits += credits
    if total_credits == 0:
        return None
    return round(total_points / total_credits, 2)
