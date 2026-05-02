from typing import Any, Dict

from pydantic import BaseModel, Field


class CheckpointCreate(BaseModel):
    project_id: str
    milestone: str = Field(..., pattern="^(plan|code|debug|test|done)$")
    state_data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CheckpointOut(CheckpointCreate):
    id: str
    created_at: str
    version: int
