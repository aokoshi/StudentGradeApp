from .person import Person


class Admin(Person):
    def __init__(self, person_id: int, name: str, username: str, password: str):
        super().__init__(person_id, name)
        self._username = username
        self._password = password

    @property
    def username(self) -> str:
        return self._username

    def verify(self, username: str, password: str) -> bool:
        return username == self._username and password == self._password

    def role(self) -> str:
        return "admin"
