from app.constants import LESSONS_DIR
from app.services.content_loader import ContentLoader
from app.services.lesson_registry import LessonRegistry


def test_registry_discovers_30_lessons() -> None:
    loader = ContentLoader(LESSONS_DIR)
    registry = LessonRegistry(LESSONS_DIR, loader)
    lessons = registry.all_lessons()
    assert len(lessons) == 30
    assert lessons[0].day == 1
    assert lessons[-1].day == 30
