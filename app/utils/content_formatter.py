import re


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
    'with open(path, "r", encoding = "utf-8") as file:': 'with open(path, "r", encoding="utf-8") as file:',
    "return [Task(** item) for item in data]": "return [Task(**item) for item in data]",
    "done: bool= False": "done: bool = False",
    "Trueand False": "True and False",
    "Trueor False": "True or False",
    "archivo.py": "archivo .py",
}

INLINE_LIST_FIXES = {
    "Devuelven True o False. - == - != - > - < - >= - <=": "Devuelven True o False.\n- ==\n- !=\n- >\n- <\n- >=\n- <=",
    "A veces necesitas convertir un valor de un tipo a otro. - int() convierte a entero - float() convierte a\ndecimal - str() convierte a texto - bool() convierte a booleano": "A veces necesitas convertir un valor de un tipo a otro.\n- int() convierte a entero\n- float() convierte a decimal\n- str() convierte a texto\n- bool() convierte a booleano",
}


def normalize_section_text(content: str) -> str:
    text = content.replace("\r\n", "\n")
    for source, target in COMMON_REPLACEMENTS.items():
        text = text.replace(source, target)
    for source, target in INLINE_LIST_FIXES.items():
        text = text.replace(source, target)

    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if re.fullmatch(r"\d+\.", stripped):
            continue
        if not stripped:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        stripped = re.sub(r"\s+", " ", stripped)
        stripped = re.sub(r"(?<=\))(?=\w)", " ", stripped)
        stripped = re.sub(r"(?<=\w)(==|!=|>=|<=)(?=\w)", r" \1 ", stripped)
        if is_code_like(stripped):
            stripped = re.sub(r"^class(?=[A-Z_])", "class ", stripped)
            stripped = re.sub(r"^def(?=[a-zA-Z_])", "def ", stripped)
            stripped = re.sub(r"(?<![=!<>])=(?!=)", " = ", stripped)
            stripped = stripped.replace(" = = ", " == ")
            stripped = stripped.replace(" ! = ", " != ")
            stripped = stripped.replace(" > = ", " >= ")
            stripped = stripped.replace(" < = ", " <= ")
            stripped = stripped.replace(" - > ", " -> ")
            stripped = stripped.replace("* *", "**")
            stripped = stripped.replace("/ /", "//")
            stripped = stripped.replace("utf - 8", "utf-8")
            stripped = stripped.replace("bool = False", "bool = False")
            stripped = stripped.replace("done: bool = False", "done: bool = False")
            stripped = re.sub(r"\s{2,}", " ", stripped)
            stripped = stripped.replace("( ", "(").replace(" )", ")")
            stripped = stripped.replace("[ ", "[").replace(" ]", "]")
        lines.append(stripped)

    normalized = "\n".join(lines).strip()
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized


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
        "path =",
        "json.",
        "@dataclass",
    )
    return (
        line.startswith(code_prefixes)
        or line.startswith(("name =", "age =", "price =", "tasks =", "student =", "product ="))
        or bool(re.match(r"^[A-Za-z_]\w*:\s*[\w\[\]]+", line))
        or " = " in line
        or line.endswith(":")
        or line.startswith(("python ", "python3 ", "pip ", "black ", "ruff ", ".venv\\", "source "))
    )


def is_heading_like(line: str) -> bool:
    if line.startswith(("- ", "* ", "+ ")):
        return False
    if is_code_like(line):
        return False
    if line.endswith((".", ",", ":", ";")):
        return False
    return len(line.split()) <= 6 and line[:1].isupper()
