from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from evo_code.runtime import EvolutionRuntime
from evo_code.types import FunctionVariant


def process_data_v1(values: list[int]) -> int:
    total = 0
    for value in values:
        total += value
    return total


def process_data_v2(values: list[int]) -> int:
    return sum(values)


runtime = EvolutionRuntime(
    target_name="process_data",
    variants=[
        FunctionVariant(name="v1_loop", func=process_data_v1),
        FunctionVariant(name="v2_sum", func=process_data_v2),
    ],
)

decision = runtime.run(sample_input=list(range(10)))
print("Selected:", decision.best.name)
print("Scores:", decision.scores)
