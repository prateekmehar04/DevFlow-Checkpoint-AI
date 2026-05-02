from datetime import datetime, timezone
from typing import Dict
from uuid import uuid4

from fastapi import HTTPException, status

from ..schemas.checkpoint import CheckpointCreate
from ..schemas.workflow import WorkflowCreate
from ..storage import store
from .checkpoint_service import CheckpointService
from .project_service import ProjectService


TRANSITIONS = {
    "plan": {"code"},
    "code": {"debug", "test"},
    "debug": {"code", "test"},
    "test": {"code", "done"},
    "done": set(),
}


class WorkflowStateManager:
    def __init__(self) -> None:
        self.projects = ProjectService()
        self.checkpoints = CheckpointService()

    def initialize_workflow(self, payload: WorkflowCreate) -> Dict:
        self.projects.get_project(payload.project_id)
        now = _now()
        workflow = {
            "id": str(uuid4()),
            "project_id": payload.project_id,
            "current_state": payload.initial_state,
            "context": payload.context,
            "state_history": [
                {"from": None, "to": payload.initial_state, "at": now, "note": "Workflow initialized"}
            ],
            "last_checkpoint_id": None,
            "created_at": now,
            "updated_at": now,
        }
        return store.insert("workflows", workflow)

    def get_workflow(self, workflow_id: str) -> Dict:
        workflow = store.get("workflows", workflow_id)
        if not workflow:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
        return workflow

    def transition_state(
        self,
        workflow_id: str,
        target_state: str,
        auto_checkpoint: bool = True,
        note: str = "",
    ) -> Dict:
        workflow = self.get_workflow(workflow_id)
        current_state = workflow["current_state"]
        if not self.validate_transition(current_state, target_state):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot transition from {current_state} to {target_state}",
            )

        checkpoint_id = workflow.get("last_checkpoint_id")
        if auto_checkpoint:
            checkpoint = self.checkpoints.create_checkpoint(
                CheckpointCreate(
                    project_id=workflow["project_id"],
                    milestone=target_state,
                    state_data={
                        "workflow_id": workflow_id,
                        "from_state": current_state,
                        "to_state": target_state,
                        "context": workflow["context"],
                    },
                    metadata={"source": "auto-transition", "note": note},
                )
            )
            checkpoint_id = checkpoint["id"]

        workflow["current_state"] = target_state
        workflow["last_checkpoint_id"] = checkpoint_id
        workflow["updated_at"] = _now()
        workflow["state_history"].append(
            {
                "from": current_state,
                "to": target_state,
                "at": workflow["updated_at"],
                "checkpoint_id": checkpoint_id,
                "note": note,
            }
        )
        return store.replace("workflows", workflow_id, workflow) or workflow

    def rollback_state(self, workflow_id: str, target_checkpoint_id: str) -> Dict:
        workflow = self.get_workflow(workflow_id)
        checkpoint = self.checkpoints.get_checkpoint(target_checkpoint_id)
        if checkpoint["project_id"] != workflow["project_id"]:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Checkpoint belongs to a different project",
            )

        previous = workflow["current_state"]
        workflow["current_state"] = checkpoint["milestone"]
        workflow["context"] = checkpoint["state_data"].get("context", checkpoint["state_data"])
        workflow["last_checkpoint_id"] = checkpoint["id"]
        workflow["updated_at"] = _now()
        workflow["state_history"].append(
            {
                "from": previous,
                "to": workflow["current_state"],
                "at": workflow["updated_at"],
                "checkpoint_id": checkpoint["id"],
                "note": "Rolled back to checkpoint",
            }
        )
        return store.replace("workflows", workflow_id, workflow) or workflow

    def validate_transition(self, current_state: str, target_state: str) -> bool:
        return target_state in TRANSITIONS.get(current_state, set())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
