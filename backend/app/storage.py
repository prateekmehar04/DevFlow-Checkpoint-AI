from __future__ import annotations

import copy
import json
from pathlib import Path
from threading import RLock
from typing import Any, Dict, List, Optional

from .config import settings


DEFAULT_STATE: Dict[str, Any] = {
    "projects": [],
    "checkpoints": [],
    "workflows": [],
    "contexts": {},
}


class JsonStore:
    def __init__(self, path: Optional[Path] = None):
        self.path = path or settings.data_path
        self._lock = RLock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(DEFAULT_STATE)

    def _read(self) -> Dict[str, Any]:
        with self._lock:
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return copy.deepcopy(DEFAULT_STATE)

    def _write(self, data: Dict[str, Any]) -> None:
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

    def all(self, collection: str) -> List[Dict[str, Any]]:
        return copy.deepcopy(self._read().get(collection, []))

    def get(self, collection: str, item_id: str) -> Optional[Dict[str, Any]]:
        return next((item for item in self.all(collection) if item["id"] == item_id), None)

    def insert(self, collection: str, item: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        data.setdefault(collection, []).append(copy.deepcopy(item))
        self._write(data)
        return copy.deepcopy(item)

    def replace(self, collection: str, item_id: str, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        data = self._read()
        items = data.setdefault(collection, [])
        for index, existing in enumerate(items):
            if existing["id"] == item_id:
                items[index] = copy.deepcopy(item)
                self._write(data)
                return copy.deepcopy(item)
        return None

    def delete(self, collection: str, item_id: str) -> bool:
        data = self._read()
        items = data.setdefault(collection, [])
        next_items = [item for item in items if item["id"] != item_id]
        if len(next_items) == len(items):
            return False
        data[collection] = next_items
        self._write(data)
        return True

    def save_context(self, workflow_id: str, context: Dict[str, Any]) -> None:
        data = self._read()
        data.setdefault("contexts", {})[workflow_id] = copy.deepcopy(context)
        self._write(data)

    def load_context(self, workflow_id: str) -> Dict[str, Any]:
        return copy.deepcopy(self._read().get("contexts", {}).get(workflow_id, {}))

    def reset(self) -> None:
        self._write(copy.deepcopy(DEFAULT_STATE))


store = JsonStore()
