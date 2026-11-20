class Task:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f"Task<{self.title}>"


print(Task("Study"))
