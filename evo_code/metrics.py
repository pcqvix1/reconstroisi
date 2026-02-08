from __future__ import annotations

import time
import tracemalloc
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Tuple

from evo_code.types import Metrics


@dataclass
class MetricsCollector:
    history: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def observe(self, name: str) -> Callable[[Callable[[Any], Any]], Callable[[Any], Tuple[Any, Metrics]]]:
        def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Tuple[Any, Metrics]]:
            def wrapper(arg: Any) -> Tuple[Any, Metrics]:
                output, metrics, error = self.measure(name, func, arg)
                if error:
                    raise error
                return output, metrics

            return wrapper

        return decorator

    def measure(self, name: str, func: Callable[[Any], Any], arg: Any) -> Tuple[Any, Metrics, Exception | None]:
        tracemalloc.start()
        start = time.perf_counter()
        output: Any = None
        error: Exception | None = None
        try:
            output = func(arg)
        except Exception as exc:  # noqa: BLE001
            error = exc
        end = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed = end - start
        record = self.history.setdefault(name, {"time_total": 0.0, "calls": 0})
        record["time_total"] += elapsed
        record["calls"] += 1

        metrics = Metrics(
            function=name,
            avg_time=record["time_total"] / record["calls"],
            memory_peak=float(peak) / (1024 * 1024),
            calls=int(record["calls"]),
        )
        return output, metrics, error
