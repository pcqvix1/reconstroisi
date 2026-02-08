from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

from evo_code.types import VariantResult


@dataclass
class HistoryEntry:
    selected: str
    scores: Dict[str, float]
    metrics: Dict[str, Any]


class HistoryStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, selected: str, scores: Dict[str, float], results: List[VariantResult]) -> None:
        entry = HistoryEntry(
            selected=selected,
            scores=scores,
            metrics={result.variant.name: asdict(result.metrics) for result in results},
        )
        history = self._read()
        history.append(asdict(entry))
        self.path.write_text(json.dumps(history, indent=2), encoding="utf-8")

    def _read(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))
