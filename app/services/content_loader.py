import json
from pathlib import Path

from app.models import CodeBlock, Lesson, LessonSection
from app.utils.file_utils import read_text_file


class ContentLoader:
    def __init__(self, lessons_dir: Path) -> None:
        self.lessons_dir = lessons_dir

    def load_lesson(self, lesson_dir: Path) -> Lesson:
        metadata = json.loads(read_text_file(lesson_dir / "lesson.json"))
        sections = [
            LessonSection(
                identifier=section["id"],
                title=section["title"],
                file_path=section["file"],
            )
            for section in metadata["sections"]
        ]
        code_blocks = [
            CodeBlock(
                identifier=block["id"],
                title=block["title"],
                category=block["category"],
                file_path=block["file"],
                description=block["description"],
                expected_output=block.get("expected_output", ""),
                default_input=block.get("default_input", ""),
            )
            for block in metadata["code_blocks"]
        ]
        return Lesson(
            day=metadata["day"],
            slug=metadata["slug"],
            title=metadata["title"],
            summary=metadata["summary"],
            sections=sections,
            code_blocks=code_blocks,
        )

    def read_section(self, lesson: Lesson, section: LessonSection) -> str:
        lesson_dir = self.lessons_dir / lesson.slug
        return read_text_file(lesson_dir / section.file_path)

    def read_code_block(self, lesson: Lesson, block: CodeBlock) -> str:
        lesson_dir = self.lessons_dir / lesson.slug
        return read_text_file(lesson_dir / block.file_path)
