import json
from pathlib import Path


class ProgressService:
    def __init__(self, storage_file: Path) -> None:
        self.storage_file = storage_file
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load()

    def _load(self) -> dict[str, list[int]]:
        if not self.storage_file.exists():
            return {"visited_days": []}
        return json.loads(self.storage_file.read_text(encoding="utf-8"))

    def save(self) -> None:
        self.storage_file.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def mark_visited(self, day: int) -> None:
        visited = set(self._data.get("visited_days", []))
        visited.add(day)
        self._data["visited_days"] = sorted(visited)
        self.save()

    def is_visited(self, day: int) -> bool:
        return day in self._data.get("visited_days", [])

    def visited_count(self) -> int:
        return len(self._data.get("visited_days", []))
