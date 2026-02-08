from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from evolver.targets import process_data_baseline


@dataclass
class RuntimeState:
    registry: dict[str, Callable[..., int]]


def create_runtime() -> RuntimeState:
    return RuntimeState(registry={"process_data": process_data_baseline})


def run(runtime: RuntimeState, name: str, *args: object) -> int:
    func = runtime.registry[name]
    return func(*args)
