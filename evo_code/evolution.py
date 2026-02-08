from __future__ import annotations

from typing import Dict, List

from evo_code.types import EvolutionDecision, FitnessWeights, FunctionVariant, Metrics, VariantResult


class EvolutionEngine:
    def __init__(self, weights: FitnessWeights | None = None) -> None:
        self.weights = weights or FitnessWeights()

    def fitness(self, baseline: Metrics, current: Metrics, stability_score: float) -> float:
        time_score = baseline.avg_time / current.avg_time if current.avg_time else 0.0
        memory_score = baseline.memory_peak / current.memory_peak if current.memory_peak else 0.0
        return (
            self.weights.time * time_score
            + self.weights.memory * memory_score
            + self.weights.stability * stability_score
        )

    def select(self, baseline: Metrics, results: List[VariantResult]) -> EvolutionDecision:
        scores: Dict[str, float] = {}
        best_variant: FunctionVariant | None = None
        best_score = float("-inf")

        for result in results:
            stability = 0.0 if result.error else 1.0
            score = self.fitness(baseline, result.metrics, stability)
            scores[result.variant.name] = score
            if score > best_score:
                best_score = score
                best_variant = result.variant

        if best_variant is None:
            raise ValueError("No variants provided for selection.")

        return EvolutionDecision(best=best_variant, score=best_score, scores=scores, results=results)
