from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Callable, Iterable


ALLOWED_NODES: tuple[type[ast.AST], ...] = (
    ast.Module,
    ast.FunctionDef,
    ast.arguments,
    ast.arg,
    ast.Return,
    ast.Assign,
    ast.AnnAssign,
    ast.For,
    ast.If,
    ast.Compare,
    ast.ListComp,
    ast.comprehension,
    ast.BinOp,
    ast.Add,
    ast.Mult,
    ast.Sub,
    ast.Div,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Call,
    ast.Attribute,
    ast.Constant,
    ast.Subscript,
    ast.List,
    ast.Tuple,
)


@dataclass
class RewriteCandidate:
    identifier: str
    func_name: str
    source: str


class CodeRewriter:
    def __init__(self, whitelist: Iterable[type[ast.AST]] = ALLOWED_NODES) -> None:
        self._whitelist = tuple(whitelist)

    def validate_ast(self, source: str) -> ast.Module:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if not isinstance(node, self._whitelist):
                raise ValueError(f"Disallowed AST node: {type(node).__name__}")
        return tree

    def compile_function(self, candidate: RewriteCandidate) -> Callable[..., int]:
        tree = self.validate_ast(candidate.source)
        compiled = compile(tree, filename=f"<candidate:{candidate.identifier}>", mode="exec")
        namespace: dict[str, Callable[..., int]] = {}
        exec(compiled, namespace)
        func = namespace.get(candidate.func_name)
        if not callable(func):
            raise ValueError(f"Candidate {candidate.identifier} did not define a callable.")
        return func
