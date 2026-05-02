from __future__ import annotations

from typing import Any, Dict, List


def calculate_diff(left: Any, right: Any, path: str = "") -> Dict[str, List[Dict[str, Any]]]:
    changes: Dict[str, List[Dict[str, Any]]] = {
        "added": [],
        "removed": [],
        "changed": [],
    }

    if isinstance(left, dict) and isinstance(right, dict):
        left_keys = set(left.keys())
        right_keys = set(right.keys())
        for key in sorted(right_keys - left_keys):
            changes["added"].append({"path": _join(path, key), "value": right[key]})
        for key in sorted(left_keys - right_keys):
            changes["removed"].append({"path": _join(path, key), "value": left[key]})
        for key in sorted(left_keys & right_keys):
            child = calculate_diff(left[key], right[key], _join(path, key))
            _extend(changes, child)
        return changes

    if isinstance(left, list) and isinstance(right, list):
        max_len = max(len(left), len(right))
        for index in range(max_len):
            item_path = f"{path}[{index}]"
            if index >= len(left):
                changes["added"].append({"path": item_path, "value": right[index]})
            elif index >= len(right):
                changes["removed"].append({"path": item_path, "value": left[index]})
            else:
                child = calculate_diff(left[index], right[index], item_path)
                _extend(changes, child)
        return changes

    if left != right:
        changes["changed"].append({"path": path or "$", "from": left, "to": right})
    return changes


def _join(path: str, key: str) -> str:
    return f"{path}.{key}" if path else str(key)


def _extend(target: Dict[str, List[Dict[str, Any]]], source: Dict[str, List[Dict[str, Any]]]) -> None:
    for bucket, values in source.items():
        target[bucket].extend(values)
