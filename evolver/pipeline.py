from __future__ import annotations

from pathlib import Path
from typing import Iterable

from evolver.deployment import DeploymentManager
from evolver.evolution import EvolutionEngine, FitnessResult
from evolver.metrics import MetricsCollector
from evolver.rewriter import CodeRewriter, RewriteCandidate
from evolver.storage import HistoryStore, VersionRecord
from evolver.validator import Validator


def _build_candidates() -> list[RewriteCandidate]:
    return [
        RewriteCandidate(
            identifier="process_data_generator",
            func_name="process_data",
            source="""
def process_data(data: list[int]) -> int:
    return sum(value * value for value in data)
""",
        ),
        RewriteCandidate(
            identifier="process_data_listcomp",
            func_name="process_data",
            source="""
def process_data(data: list[int]) -> int:
    return sum([value * value for value in data])
""",
        ),
    ]


def evolve(
    runtime_registry: dict[str, callable],
    inputs: Iterable[tuple],
    history_path: Path,
) -> FitnessResult:
    collector = MetricsCollector()
    validator = Validator(oracle=runtime_registry["process_data"])
    engine = EvolutionEngine()
    rewriter = CodeRewriter()

    baseline_metrics = collector.observe(runtime_registry["process_data"], inputs)
    results: list[FitnessResult] = []

    candidates = _build_candidates()
    for candidate in candidates:
        func = rewriter.compile_function(candidate)
        validation = validator.validate(func, inputs)
        if not validation.ok:
            continue
        metrics = engine.measure(collector, func, inputs)
        result = engine.evaluate(
            baseline=baseline_metrics,
            stability_score=1.0,
            candidate_name=candidate.identifier,
            metrics=metrics,
        )
        results.append(result)

    if not results:
        raise RuntimeError("No viable candidates.")

    best = engine.select_best(results)
    deployment = DeploymentManager(runtime_registry)
    best_candidate = next(c for c in candidates if c.identifier == best.candidate_name)
    deployment.hot_swap("process_data", rewriter.compile_function(best_candidate))
    HistoryStore(history_path).append(
        VersionRecord(
            version_id="v1",
            candidate_name=best.candidate_name,
            fitness=best.fitness,
            metrics=best.metrics,
        )
    )
    return best
