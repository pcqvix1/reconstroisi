from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from evolver.metrics import MetricsSnapshot


@dataclass
class VersionRecord:
    version_id: str
    candidate_name: str
    fitness: float
    metrics: MetricsSnapshot


class HistoryStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: VersionRecord) -> None:
        payload = asdict(record)
        payload["metrics"]["samples"] = payload["metrics"]["samples"][:10]
        payload["timestamp"] = datetime.now(timezone.utc).isoformat()
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")
