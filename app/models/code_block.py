from dataclasses import dataclass


@dataclass(frozen=True)
class CodeBlock:
    identifier: str
    title: str
    category: str
    file_path: str
    description: str
    expected_output: str = ""
    default_input: str = ""
