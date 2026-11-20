from dataclasses import dataclass

from .code_block import CodeBlock


@dataclass(frozen=True)
class LessonSection:
    identifier: str
    title: str
    file_path: str


@dataclass(frozen=True)
class Lesson:
    day: int
    slug: str
    title: str
    summary: str
    sections: list[LessonSection]
    code_blocks: list[CodeBlock]
