from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    tech_stack: Dict[str, Any] = Field(default_factory=dict)
    status: str = "active"


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    tech_stack: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ProjectOut(ProjectCreate):
    id: str
    created_at: str
    updated_at: str
