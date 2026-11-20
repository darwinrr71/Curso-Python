class Progress:
    def __init__(self, completed_days: int) -> None:
        self.completed_days = completed_days


class Course:
    def __init__(self, title: str, progress: Progress) -> None:
        self.title = title
        self.progress = progress


course = Course("Python", Progress(24))
print(course.title, course.progress.completed_days)
