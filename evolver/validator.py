from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass
class ValidationResult:
    ok: bool
    details: str


class Validator:
    def __init__(self, oracle: Callable[..., int]) -> None:
        self._oracle = oracle

    def validate(self, func: Callable[..., int], inputs: Iterable[tuple]) -> ValidationResult:
        for args in inputs:
            expected = self._oracle(*args)
            actual = func(*args)
            if expected != actual:
                return ValidationResult(
                    ok=False,
                    details=f"Mismatch for args={args}: expected={expected} got={actual}",
                )
        return ValidationResult(ok=True, details="All checks passed.")
