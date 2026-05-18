class Course:
    def __init__(self, code: str, title: str, credits: int = 3):
        if not code or not code.strip():
            raise ValueError("code must be non-empty")
        if credits <= 0:
            raise ValueError("credits must be positive")
        self.code = code.strip()
        self.title = title.strip()
        self.credits = int(credits)

    def __eq__(self, other) -> bool:
        return isinstance(other, Course) and self.code == other.code

    def __hash__(self) -> int:
        return hash(self.code)

    def __repr__(self) -> str:
        return f"Course(code={self.code!r}, title={self.title!r}, credits={self.credits})"
