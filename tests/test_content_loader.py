from app.constants import LESSONS_DIR
from app.services.content_loader import ContentLoader
from app.services.lesson_registry import LessonRegistry


def test_content_loader_reads_lesson_sections() -> None:
    loader = ContentLoader(LESSONS_DIR)
    registry = LessonRegistry(LESSONS_DIR, loader)
    lesson = registry.get_by_day(1)
    section_content = loader.read_section(lesson, lesson.sections[0])
    assert lesson.title.startswith("Qué es Python")
    assert "hoy vas a entender" in section_content.lower()
