def build_message(name: str) -> str:
    return f"Hello, {name}"


def test_build_message() -> None:
    assert build_message("Ada") == "Hello, Ada"


test_build_message()
print("pytest-style test passed")
