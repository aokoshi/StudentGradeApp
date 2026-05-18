class Grade:
    LETTER_BOUNDS = (
        (90, "A", 4.0),
        (80, "B", 3.0),
        (70, "C", 2.0),
        (60, "D", 1.0),
        (0,  "F", 0.0),
    )

    def __init__(self, student_id: int, course_code: str, score: float):
        if not 0 <= score <= 100:
            raise ValueError("score must be in [0, 100]")
        self.student_id = int(student_id)
        self.course_code = course_code.strip()
        self.score = float(score)

    @property
    def letter(self) -> str:
        for cutoff, letter, _ in self.LETTER_BOUNDS:
            if self.score >= cutoff:
                return letter
        return "F"

    @property
    def gpa_points(self) -> float:
        for cutoff, _, points in self.LETTER_BOUNDS:
            if self.score >= cutoff:
                return points
        return 0.0

    def __repr__(self) -> str:
        return (
            f"Grade(student_id={self.student_id}, course={self.course_code!r}, "
            f"score={self.score}, letter={self.letter})"
        )
