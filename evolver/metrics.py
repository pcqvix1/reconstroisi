from __future__ import annotations

import statistics
import time
import tracemalloc
from dataclasses import dataclass, field
from typing import Callable, Iterable


@dataclass
class MetricsSnapshot:
    function: str
    avg_time: float
    p95_time: float
    p99_time: float
    memory_peak: float
    calls: int
    samples: list[float] = field(default_factory=list)


class MetricsCollector:
    def __init__(self) -> None:
        self._records: list[MetricsSnapshot] = []

    def observe(self, func: Callable[..., int], inputs: Iterable[tuple], runs: int = 10) -> MetricsSnapshot:
        timings: list[float] = []
        tracemalloc.start()
        for _ in range(runs):
            for args in inputs:
                start = time.perf_counter()
                func(*args)
                timings.append(time.perf_counter() - start)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        timings_sorted = sorted(timings)
        avg_time = statistics.mean(timings_sorted)
        p95_time = timings_sorted[int(len(timings_sorted) * 0.95) - 1]
        p99_time = timings_sorted[int(len(timings_sorted) * 0.99) - 1]
        snapshot = MetricsSnapshot(
            function=func.__name__,
            avg_time=avg_time,
            p95_time=p95_time,
            p99_time=p99_time,
            memory_peak=peak / 1024 / 1024,
            calls=len(timings_sorted),
            samples=timings_sorted,
        )
        self._records.append(snapshot)
        return snapshot

    @property
    def records(self) -> list[MetricsSnapshot]:
        return list(self._records)
