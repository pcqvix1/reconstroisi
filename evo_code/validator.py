from __future__ import annotations

import ast
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import Any

from evo_code.rewriter import CodeRewrite


@dataclass
class ValidationResult:
    ok: bool
    error: str | None = None


class Validator:
    def __init__(self, target_name: str, timeout_s: float = 2.0) -> None:
        self.timeout_s = timeout_s
        self.target_name = target_name

    def validate(self, rewrite: CodeRewrite, sample_input: Any) -> ValidationResult:
        try:
            ast.parse(rewrite.source)
        except SyntaxError as exc:
            return ValidationResult(ok=False, error=f"syntax: {exc}")

        program = self._sandbox_program(rewrite.source, sample_input)
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as handle:
            handle.write(program)
            handle.flush()
            path = handle.name

        try:
            subprocess.run(
                [sys.executable, path],
                check=True,
                timeout=self.timeout_s,
                capture_output=True,
                text=True,
            )
        except subprocess.TimeoutExpired:
            return ValidationResult(ok=False, error="timeout")
        except subprocess.CalledProcessError as exc:
            return ValidationResult(ok=False, error=exc.stderr.strip() or "runtime error")

        return ValidationResult(ok=True)

    def _sandbox_program(self, source: str, sample_input: Any) -> str:
        return (
            f"{source}\n"
            f"if __name__ == '__main__':\n"
            f"    {self._sample_arg_name()} = {self._serialize(sample_input)}\n"
            f"    {self._target_call()}\n"
        )

    def _serialize(self, value: Any) -> str:
        return repr(value)

    def _target_call(self) -> str:
        return f"{self._target_name()}({self._sample_arg_name()})"

    def _target_name(self) -> str:
        return self.target_name

    def _sample_arg_name(self) -> str:
        return "input_value"
