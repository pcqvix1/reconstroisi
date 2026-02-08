from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class DeploymentResult:
    ok: bool
    details: str


class DeploymentManager:
    def __init__(self, registry: dict[str, Callable[..., int]]) -> None:
        self._registry = registry

    def hot_swap(self, name: str, func: Callable[..., int]) -> DeploymentResult:
        if name not in self._registry:
            return DeploymentResult(ok=False, details=f"Unknown target {name}")
        self._registry[name] = func
        return DeploymentResult(ok=True, details=f"Swapped implementation for {name}")
