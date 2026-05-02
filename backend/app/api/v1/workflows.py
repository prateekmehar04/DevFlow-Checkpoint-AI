from fastapi import APIRouter, status

from ...schemas.workflow import WorkflowCreate, WorkflowOut, WorkflowRollbackRequest, WorkflowTransitionRequest
from ...services.state_manager import WorkflowStateManager

router = APIRouter(prefix="/workflows", tags=["workflows"])
manager = WorkflowStateManager()


@router.post("", response_model=WorkflowOut, status_code=status.HTTP_201_CREATED)
def initialize_workflow(payload: WorkflowCreate):
    return manager.initialize_workflow(payload)


@router.get("/{workflow_id}", response_model=WorkflowOut)
def get_workflow(workflow_id: str):
    return manager.get_workflow(workflow_id)


@router.post("/{workflow_id}/transition", response_model=WorkflowOut)
def transition_workflow(workflow_id: str, payload: WorkflowTransitionRequest):
    return manager.transition_state(workflow_id, payload.target_state, payload.auto_checkpoint, payload.note)


@router.post("/{workflow_id}/rollback", response_model=WorkflowOut)
def rollback_workflow(workflow_id: str, payload: WorkflowRollbackRequest):
    return manager.rollback_state(workflow_id, payload.target_checkpoint_id)


@router.get("/{workflow_id}/history")
def get_workflow_history(workflow_id: str):
    return {"workflow_id": workflow_id, "history": manager.get_workflow(workflow_id)["state_history"]}
