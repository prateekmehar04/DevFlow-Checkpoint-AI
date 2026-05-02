from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WorkflowCreate(BaseModel):
    project_id: str
    initial_state: str = Field(default="plan", pattern="^(plan|code|debug|test|done)$")
    context: Dict[str, Any] = Field(default_factory=dict)


class WorkflowTransitionRequest(BaseModel):
    target_state: str = Field(..., pattern="^(plan|code|debug|test|done)$")
    auto_checkpoint: bool = True
    note: str = ""


class WorkflowRollbackRequest(BaseModel):
    target_checkpoint_id: str


class WorkflowOut(BaseModel):
    id: str
    project_id: str
    current_state: str
    context: Dict[str, Any]
    state_history: List[Dict[str, Any]]
    last_checkpoint_id: Optional[str] = None
    created_at: str
    updated_at: str
