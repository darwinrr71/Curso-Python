class Task:
    def __init__(self, title, done=False):
        self.title = title
        self.done = done

    def mark_done(self):
        self.done = True

    def __str__(self):
        status = "done" if self.done else "pending"
        return f"Task: {self.title} ({status})"
