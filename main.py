from __future__ import annotations

from pathlib import Path

from evolver.pipeline import evolve
from evolver.runtime import create_runtime, run


def main() -> None:
    runtime = create_runtime()
    inputs = [
        ([1, 2, 3, 4, 5],),
        ([10, 20, 30, 40],),
        (list(range(100)),),
    ]
    result = evolve(runtime.registry, inputs, Path("history/versions.jsonl"))
    output = run(runtime, "process_data", list(range(10)))
    print(f"Best candidate: {result.candidate_name} fitness={result.fitness:.3f}")
    print(f"Sample output: {output}")


if __name__ == "__main__":
    main()
