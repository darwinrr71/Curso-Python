import builtins
import contextlib
import io
import traceback
from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionResult:
    stdout: str
    stderr: str
    success: bool


class CodeRunner:
    def execute(self, code: str, stdin_text: str = "") -> ExecutionResult:
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        inputs = stdin_text.splitlines()
        input_index = 0

        def patched_input(prompt: str = "") -> str:
            nonlocal input_index
            if prompt:
                print(prompt, end="")
            if input_index >= len(inputs):
                raise EOFError("No more input values were provided for input().")
            value = inputs[input_index]
            input_index += 1
            print(value)
            return value

        sandbox_builtins = dict(vars(builtins))
        sandbox_builtins["input"] = patched_input

        namespace = {
            "__builtins__": sandbox_builtins,
            "__name__": "__main__",
        }
        success = True

        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            try:
                exec(compile(code, "<lesson-snippet>", "exec"), namespace, namespace)
            except Exception:
                success = False
                traceback.print_exc()

        return ExecutionResult(
            stdout=stdout_buffer.getvalue(),
            stderr=stderr_buffer.getvalue(),
            success=success,
        )
