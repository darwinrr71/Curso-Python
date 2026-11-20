from app.models import Lesson
from app.services.navigation_service import NavigationService


def test_navigation_service_moves_between_days() -> None:
    lessons = [
        Lesson(day=1, slug="dia_01", title="A", summary="", sections=[], code_blocks=[]),
        Lesson(day=2, slug="dia_02", title="B", summary="", sections=[], code_blocks=[]),
        Lesson(day=5, slug="dia_05", title="C", summary="", sections=[], code_blocks=[]),
    ]
    navigation = NavigationService(lessons)
    assert navigation.previous_day(2) == 1
    assert navigation.next_day(2) == 5
    assert navigation.previous_day(1) is None
