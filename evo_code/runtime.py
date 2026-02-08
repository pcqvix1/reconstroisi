from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, List

from evo_code.evolution import EvolutionEngine
from evo_code.metrics import MetricsCollector
from evo_code.rewriter import CodeRewriter
from evo_code.storage import HistoryStore
from evo_code.types import EvolutionDecision, FunctionVariant, VariantResult
from evo_code.validator import Validator


@dataclass
class EvolutionRuntime:
    target_name: str
    variants: List[FunctionVariant]
    history_path: Path = Path(".evolution/history.json")

    def run(self, sample_input: Any, baseline_index: int = 0) -> EvolutionDecision:
        collector = MetricsCollector()
        engine = EvolutionEngine()
        validator = Validator(self.target_name)
        rewriter = CodeRewriter(self.target_name)
        history = HistoryStore(self.history_path)

        results = self._evaluate_variants(collector, sample_input)
        baseline = results[baseline_index].metrics

        decision = engine.select(baseline, results)
        rewrite = rewriter.rewrite(decision.best)
        validation = validator.validate(rewrite, sample_input)
        if not validation.ok:
            raise RuntimeError(f"Validation failed: {validation.error}")

        history.append(decision.best.name, decision.scores, results)
        return decision

    def _evaluate_variants(
        self,
        collector: MetricsCollector,
        sample_input: Any,
    ) -> List[VariantResult]:
        results: List[VariantResult] = []
        for variant in self.variants:
            output, metrics, error = collector.measure(variant.name, variant.func, sample_input)
            results.append(
                VariantResult(
                    variant=variant,
                    metrics=metrics,
                    output=output,
                    error=str(error) if error else None,
                )
            )
        return results
