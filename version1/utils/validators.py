import re

_EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
_COURSE_CODE_RE = re.compile(r"^[A-Z]{2,4}\d{3,4}$")


def is_valid_email(value: str) -> bool:
    return bool(_EMAIL_RE.match(value or ""))


def is_valid_score(value) -> bool:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return False
    return 0 <= score <= 100


def is_valid_course_code(value: str) -> bool:
    """Course codes like CS101, MATH2010."""
    return bool(_COURSE_CODE_RE.match(value or ""))
