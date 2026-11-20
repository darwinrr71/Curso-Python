from app.services.code_runner import CodeRunner


def test_code_runner_captures_stdout_and_stderr() -> None:
    runner = CodeRunner()
    result = runner.execute('print("hola")\nraise ValueError("boom")')
    assert "hola" in result.stdout
    assert "ValueError" in result.stderr
    assert result.success is False


def test_code_runner_supports_input() -> None:
    runner = CodeRunner()
    result = runner.execute('name = input("Nombre: ")\nprint(name.upper())', "ada")
    assert "Nombre: ada" in result.stdout
    assert "ADA" in result.stdout
