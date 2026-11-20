from app.models import Lesson


class NavigationService:
    def __init__(self, lessons: list[Lesson]) -> None:
        self.lessons = lessons
        self._days = {lesson.day for lesson in lessons}
        self._sorted_days = sorted(self._days)

    def previous_day(self, day: int) -> int | None:
        previous_days = [item for item in self._days if item < day]
        return max(previous_days) if previous_days else None

    def next_day(self, day: int) -> int | None:
        next_days = [item for item in self._days if item > day]
        return min(next_days) if next_days else None

    def first_day(self) -> int | None:
        return self._sorted_days[0] if self._sorted_days else None

    def last_day(self) -> int | None:
        return self._sorted_days[-1] if self._sorted_days else None
