class User:
    def __init__(self, username: str, active: bool = True) -> None:
        self.username = username
        self.active = active

    def deactivate(self) -> None:
        self.active = False


user = User("darwin")
user.deactivate()
print(user.username, user.active)
