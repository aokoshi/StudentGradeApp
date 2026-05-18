class Person:
    def __init__(self, person_id: int, name: str):
        if not name or not name.strip():
            raise ValueError("name must be non-empty")
        self._id = int(person_id)
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def role(self) -> str:
        return "person"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self._id}, name={self._name!r})"
