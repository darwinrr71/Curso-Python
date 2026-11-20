from dataclasses import dataclass


@dataclass
class LessonCard:
    day: int
    title: str
    estimated_minutes: int


print(LessonCard(25, "Dataclass y type hints", 75))
