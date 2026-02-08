from __future__ import annotations

import ast
import inspect
import textwrap
from dataclasses import dataclass
from typing import Callable

from evo_code.types import FunctionVariant


@dataclass
class CodeRewrite:
    name: str
    source: str


class CodeRewriter:
    def __init__(self, target_name: str) -> None:
        self.target_name = target_name

    def to_ast(self, func: Callable[[object], object]) -> ast.FunctionDef:
        source = ast.get_source_segment(func.__code__, func.__code__.co_firstlineno)
        if source is None:
            source = ast.unparse(ast.parse(self._simple_stub(func)))
        node = ast.parse(source).body[0]
        if not isinstance(node, ast.FunctionDef):
            raise ValueError("Provided source does not define a function.")
        return node

    def _simple_stub(self, func: Callable[[object], object]) -> str:
        return f"def {func.__name__}(x):\n    return ({func.__name__})(x)\n"

    def rewrite(self, variant: FunctionVariant) -> CodeRewrite:
        source = ast.unparse(ast.parse(self._variant_source(variant)))
        return CodeRewrite(name=variant.name, source=source)

    def _variant_source(self, variant: FunctionVariant) -> str:
        variant_source = textwrap.dedent(inspect.getsource(variant.func))
        return (
            f"{variant_source}\n\n"
            f"def {self.target_name}(x):\n"
            f"    return {variant.func.__name__}(x)\n"
        )
