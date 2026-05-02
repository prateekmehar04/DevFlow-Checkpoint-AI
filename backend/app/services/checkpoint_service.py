from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import HTTPException, status

from ..schemas.checkpoint import CheckpointCreate
from ..storage import store
from ..utils.diff_calculator import calculate_diff
from .project_service import ProjectService


class CheckpointService:
    def __init__(self) -> None:
        self.projects = ProjectService()

    def create_checkpoint(self, payload: CheckpointCreate) -> Dict:
        self.projects.get_project(payload.project_id)
        project_checkpoints = self.list_checkpoints(payload.project_id)
        checkpoint = {
            "id": str(uuid4()),
            "project_id": payload.project_id,
            "milestone": payload.milestone,
            "state_data": payload.state_data,
            "metadata": payload.metadata,
            "version": len(project_checkpoints) + 1,
            "created_at": _now(),
        }
        return store.insert("checkpoints", checkpoint)

    def get_checkpoint(self, checkpoint_id: str) -> Dict:
        checkpoint = store.get("checkpoints", checkpoint_id)
        if not checkpoint:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Checkpoint not found")
        return checkpoint

    def list_checkpoints(self, project_id: str, milestone: Optional[str] = None) -> List[Dict]:
        checkpoints = [item for item in store.all("checkpoints") if item["project_id"] == project_id]
        if milestone:
            checkpoints = [item for item in checkpoints if item["milestone"] == milestone]
        return sorted(checkpoints, key=lambda item: item["created_at"])

    def restore_checkpoint(self, checkpoint_id: str) -> Dict:
        checkpoint = self.get_checkpoint(checkpoint_id)
        return {
            "checkpoint_id": checkpoint["id"],
            "project_id": checkpoint["project_id"],
            "milestone": checkpoint["milestone"],
            "version": checkpoint["version"],
            "state_data": checkpoint["state_data"],
        }

    def calculate_checkpoint_diff(self, left_id: str, right_id: str) -> Dict:
        left = self.get_checkpoint(left_id)
        right = self.get_checkpoint(right_id)
        return {
            "from_checkpoint_id": left_id,
            "to_checkpoint_id": right_id,
            "diff": calculate_diff(left["state_data"], right["state_data"]),
        }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
