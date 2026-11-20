from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = ROOT / "dias"
PDF_TEXT_PATH = ROOT / "tmp_manual_pdf_text.txt"
sys.path.insert(0, str(ROOT))


DAY_PATTERN = re.compile(r"Día\s+(\d+)\s+—\s+(.+?)(?=\nObjetivo del día\n)", re.S)

SECTION_SPECS = [
    ("objective", "Objetivo del día", "sections/objective.md"),
    ("theory", "Explicación teórica completa", "sections/theory.md"),
    ("syntax", "Sintaxis y funcionamiento", "sections/syntax.md"),
    ("simple_examples", "Ejemplos simples", "sections/simple_examples.md"),
    ("practical_examples", "Ejemplos prácticos", "sections/practical_examples.md"),
    ("common_errors", "Errores comunes del principiante", "sections/common_errors.md"),
    ("best_practices", "Buenas prácticas del día", "sections/best_practices.md"),
    ("exercises", "Ejercicios para practicar", "sections/exercises.md"),
    ("challenge", "Mini reto del día", "sections/challenge.md"),
    (
        "expected_result",
        "Resultado esperado al terminar el día",
        "sections/expected_result.md",
    ),
    ("summary", "Resumen final del día", "sections/summary.md"),
]

HEADING_TO_ID = {heading: identifier for identifier, heading, _ in SECTION_SPECS}
HEADING_ORDER = [heading for _, heading, _ in SECTION_SPECS]
FILE_BY_SECTION = {identifier: file_path for identifier, _, file_path in SECTION_SPECS}

COMMON_REPLACEMENTS = {
    "pythonmain.py": "python main.py",
    "python3main.py": "python3 main.py",
    "python-mvenv.venv": "python -m venv .venv",
    "source.venv/bin/activate": "source .venv/bin/activate",
    "pipinstallrequests": "pip install requests",
    "pipfreeze> requirements.txt": "pip freeze > requirements.txt",
    "pipinstallblackruff": "pip install black ruff",
    "ruffcheck.": "ruff check .",
    "black.": "black .",
    "fromdataclassesimportdataclass": "from dataclasses import dataclass",
    "fromservicesimportadd_task": "from services import add_task",
    "fromservicesimportadd_task, list_tasks": "from services import add_task, list_tasks",
    "assertlen(tasks) ==1": "assert len(tasks) == 1",
    'asserttasks[0].title=="Study Python"': 'assert tasks[0].title == "Study Python"',
    "asserttasks[0].doneisFalse": "assert tasks[0].done is False",
    "deftest_add_task():": "def test_add_task():",
    "importjson": "import json",
    "frompathlibimportPath": "from pathlib import Path",
    "frommodelsimportTask": "from models import Task",
    "defload_tasks(filename: str) ->list[Task]:": "def load_tasks(filename: str) -> list[Task]:",
    "return[]": "return []",
    "tasks= []": "tasks = []",
    "path= Path(filename)": "path = Path(filename)",
    "data= json.load(file)": "data = json.load(file)",
    "ifnotpath.exists():": "if not path.exists():",
    'withopen(path, "r", encoding="utf-8") asfile:': 'with open(path, "r", encoding="utf-8") as file:',
    'withopen("user.json", "r", encoding="utf-8") asfile:': 'with open("user.json", "r", encoding="utf-8") as file:',
    'withopen("user.json", "w", encoding="utf-8") asfile:': 'with open("user.json", "w", encoding="utf-8") as file:',
    'withopen("tasks.json", "r", encoding="utf-8") asfile:': 'with open("tasks.json", "r", encoding="utf-8") as file:',
    'withopen("hello.txt", "w", encoding="utf-8") asfile:': 'with open("hello.txt", "w", encoding="utf-8") as file:',
    'withopen("hello.txt", "r", encoding="utf-8") asfile:': 'with open("hello.txt", "r", encoding="utf-8") as file:',
    'withopen("notes.txt", "r", encoding="utf-8") asfile:': 'with open("notes.txt", "r", encoding="utf-8") as file:',
    'withopen(filename, "w", encoding="utf-8") asfile:': 'with open(filename, "w", encoding="utf-8") as file:',
    "return[Task(**item) foritemindata]": "return [Task(**item) for item in data]",
    "TrueandFalse": "True and False",
    "TrueorFalse": "True or False",
    "notTrue": "not True",
    "print(5 = = 5)": "print(5 == 5)",
    "print(5 ! = 3)": "print(5 != 3)",
    "archivo.py": "archivo .py",
}


@dataclass
class ParsedDay:
    day: int
    title: str
    sections: dict[str, str]


def load_pdf_text() -> str:
    text = PDF_TEXT_PATH.read_text(encoding="utf-8").replace("\r\n", "\n")
    text = re.sub(r"^===== PAGE \d+ =====\s*$", "", text, flags=re.M)
    text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def parse_days(text: str) -> list[ParsedDay]:
    matches = list(DAY_PATTERN.finditer(text))
    parsed_days: list[ParsedDay] = []

    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end]
        parsed_days.append(
            ParsedDay(
                day=int(match.group(1)),
                title=re.sub(r"\s+", " ", match.group(2)).strip(),
                sections=parse_sections(body),
            )
        )

    return parsed_days


def parse_sections(day_text: str) -> dict[str, str]:
    positions: list[tuple[int, str]] = []
    for heading in HEADING_ORDER:
        match = re.search(rf"^{re.escape(heading)}\s*$", day_text, re.M)
        if match:
            positions.append((match.start(), heading))
    positions.sort()

    sections: dict[str, str] = {}
    for index, (start, heading) in enumerate(positions):
        content_start = start + len(heading)
        if day_text[content_start:content_start + 2] == "\r\n":
            content_start += 2
        elif day_text[content_start:content_start + 1] == "\n":
            content_start += 1
        content_end = positions[index + 1][0] if index + 1 < len(positions) else len(day_text)
        raw_content = day_text[content_start:content_end].strip()
        sections[HEADING_TO_ID[heading]] = format_section_text(raw_content)
    return sections


def format_section_text(raw_text: str) -> str:
    text = raw_text
    for source, target in COMMON_REPLACEMENTS.items():
        text = text.replace(source, target)

    text = re.sub(r"\u00a0", " ", text)
    lines = [line.strip() for line in text.splitlines()]

    blocks: list[str] = []
    prose: list[str] = []
    code: list[str] = []

    def flush_prose() -> None:
        if prose:
            paragraph = " ".join(prose).strip()
            paragraph = re.sub(r"\s+([.,;:!?])", r"\1", paragraph)
            blocks.append(paragraph)
            prose.clear()

    def flush_code() -> None:
        if code:
            blocks.append("\n".join(code).strip())
            code.clear()

    for line in lines:
        if not line or line == "•" or re.fullmatch(r"\d+\.", line):
            flush_prose()
            flush_code()
            continue

        if is_heading_like(line):
            flush_prose()
            flush_code()
            blocks.append(line)
            continue

        if is_code_like(line):
            flush_prose()
            code.append(normalize_code_line(line))
            continue

        flush_code()
        prose.append(re.sub(r"\s+", " ", line))

    flush_prose()
    flush_code()
    return "\n\n".join(block for block in blocks if block).strip()


def is_code_like(line: str) -> bool:
    code_prefixes = (
        "print(",
        "if ",
        "elif ",
        "else:",
        "for ",
        "while ",
        "def ",
        "class ",
        "return ",
        "import ",
        "from ",
        "with ",
        "json.",
        "@dataclass",
        "python ",
        "python3 ",
        "pip ",
        "black ",
        "ruff ",
    )
    return (
        line.startswith(code_prefixes)
        or bool(re.match(r"^[A-Za-z_][\w.]*\s*=", line))
        or bool(re.match(r"^[A-Za-z_][\w.]*\([^)]*\)$", line))
        or line.startswith(("classUser", "classProduct", "classAnimal", "classDog", "classEngine", "classCar"))
        or line.startswith(("def__", "defspeak", "defapply_", "defstart", "deftest_", "defload_"))
    )


def is_heading_like(line: str) -> bool:
    if is_code_like(line):
        return False
    if line.startswith(("- ", "* ", "+ ")):
        return False
    if line.endswith((".", ",", ";")):
        return False
    return len(line.split()) <= 8 and line[:1].isupper()


def normalize_code_line(line: str) -> str:
    fixed = line.strip()
    for source, target in COMMON_REPLACEMENTS.items():
        fixed = fixed.replace(source, target)
    fixed = re.sub(r"^class(?=[A-Z_])", "class ", fixed)
    fixed = re.sub(r"^def(?=[a-zA-Z_])", "def ", fixed)
    fixed = fixed.replace("def__", "def __")
    fixed = re.sub(r"^class([A-Z][A-Za-z0-9_]*)\(", r"class \1(", fixed)
    fixed = re.sub(r"^class([A-Z][A-Za-z0-9_]*):", r"class \1:", fixed)
    fixed = re.sub(r"^def([a-zA-Z_][A-Za-z0-9_]*)\(", r"def \1(", fixed)
    fixed = re.sub(r"(?<![=!<>])=(?!=)", " = ", fixed)
    fixed = fixed.replace(" = = ", " == ")
    fixed = fixed.replace(" ! = ", " != ")
    fixed = fixed.replace(" > = ", " >= ")
    fixed = fixed.replace(" < = ", " <= ")
    fixed = fixed.replace(" - > ", " -> ")
    fixed = fixed.replace("* *", "**")
    fixed = fixed.replace("/ /", "//")
    fixed = fixed.replace("utf - 8", "utf-8")
    fixed = re.sub(r"([+\-*/])(?=\d)", r" \1 ", fixed)
    fixed = re.sub(r"\s{2,}", " ", fixed)
    fixed = fixed.replace("( ", "(").replace(" )", ")")
    fixed = fixed.replace("[ ", "[").replace(" ]", "]")
    return fixed.strip()


def update_lesson(day: ParsedDay) -> None:
    lesson_dir = LESSONS_DIR / f"dia_{day.day:02d}"
    metadata_path = lesson_dir / "lesson.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    metadata["title"] = day.title
    metadata["summary"] = first_paragraph(day.sections.get("summary", ""))

    for section_id, _, relative_path in SECTION_SPECS:
        target = lesson_dir / relative_path
        target.write_text(day.sections.get(section_id, "").strip() + "\n", encoding="utf-8")

    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def first_paragraph(section_text: str) -> str:
    paragraphs = [part.strip().replace("\n", " ") for part in section_text.split("\n\n") if part.strip()]
    return paragraphs[0] if paragraphs else ""


def main() -> None:
    parsed_days = parse_days(load_pdf_text())
    for day in parsed_days:
        update_lesson(day)


if __name__ == "__main__":
    main()
