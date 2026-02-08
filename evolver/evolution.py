from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from evolver.metrics import MetricsCollector, MetricsSnapshot


@dataclass
class FitnessResult:
    candidate_name: str
    fitness: float
    metrics: MetricsSnapshot


class EvolutionEngine:
    def __init__(self, w_time: float = 0.6, w_memory: float = 0.3, w_stability: float = 0.1) -> None:
        self._w_time = w_time
        self._w_memory = w_memory
        self._w_stability = w_stability

    def evaluate(
        self,
        baseline: MetricsSnapshot,
        stability_score: float,
        candidate_name: str,
        metrics: MetricsSnapshot,
    ) -> FitnessResult:
        fitness = (
            self._w_time * (baseline.avg_time / metrics.avg_time)
            + self._w_memory * (baseline.memory_peak / max(metrics.memory_peak, 1e-9))
            + self._w_stability * stability_score
        )
        return FitnessResult(candidate_name=candidate_name, fitness=fitness, metrics=metrics)

    def select_best(self, results: Iterable[FitnessResult]) -> FitnessResult:
        return max(results, key=lambda item: item.fitness)

    def measure(self, collector: MetricsCollector, func: Callable[..., int], inputs: Iterable[tuple]) -> MetricsSnapshot:
        return collector.observe(func, inputs)
