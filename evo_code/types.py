from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass(frozen=True)
class Metrics:
    function: str
    avg_time: float
    memory_peak: float
    calls: int


@dataclass(frozen=True)
class VariantResult:
    variant: "FunctionVariant"
    metrics: Metrics
    output: Any
    error: str | None = None


@dataclass
class FitnessWeights:
    time: float = 0.5
    memory: float = 0.3
    stability: float = 0.2


@dataclass
class FunctionVariant:
    name: str
    func: Callable[[Any], Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvolutionDecision:
    best: FunctionVariant
    score: float
    scores: Dict[str, float]
    results: List[VariantResult]
