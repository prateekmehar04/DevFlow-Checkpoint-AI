from typing import List, Optional

from fastapi import APIRouter, Query, status

from ...schemas.checkpoint import CheckpointCreate, CheckpointOut
from ...services.checkpoint_service import CheckpointService

router = APIRouter(tags=["checkpoints"])
service = CheckpointService()


@router.post("/checkpoints", response_model=CheckpointOut, status_code=status.HTTP_201_CREATED)
def create_checkpoint(payload: CheckpointCreate):
    return service.create_checkpoint(payload)


@router.get("/checkpoints/diff")
def diff_checkpoints(left_id: str = Query(...), right_id: str = Query(...)):
    return service.calculate_checkpoint_diff(left_id, right_id)


@router.get("/checkpoints/{checkpoint_id}", response_model=CheckpointOut)
def get_checkpoint(checkpoint_id: str):
    return service.get_checkpoint(checkpoint_id)


@router.get("/projects/{project_id}/checkpoints", response_model=List[CheckpointOut])
def list_project_checkpoints(project_id: str, milestone: Optional[str] = None):
    return service.list_checkpoints(project_id, milestone)


@router.post("/checkpoints/{checkpoint_id}/restore")
def restore_checkpoint(checkpoint_id: str):
    return service.restore_checkpoint(checkpoint_id)
