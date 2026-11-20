from pathlib import Path

from app.models import Lesson
from app.services.content_loader import ContentLoader


class LessonRegistry:
    def __init__(self, lessons_dir: Path, loader: ContentLoader) -> None:
        self.lessons_dir = lessons_dir
        self.loader = loader
        self._lessons: list[Lesson] | None = None

    def all_lessons(self) -> list[Lesson]:
        if self._lessons is None:
            lesson_dirs = sorted(path for path in self.lessons_dir.glob("dia_*") if path.is_dir())
            self._lessons = [self.loader.load_lesson(path) for path in lesson_dirs]
        return list(self._lessons)

    def get_by_day(self, day: int) -> Lesson:
        for lesson in self.all_lessons():
            if lesson.day == day:
                return lesson
        raise KeyError(f"Lesson for day {day} not found.")
