from typing import Any, Dict

from pydantic import BaseModel, Field


class BobPlanRequest(BaseModel):
    project_description: str = Field(..., min_length=1)
    context: Dict[str, Any] = Field(default_factory=dict)


class BobDebugRequest(BaseModel):
    code: str
    error: str = Field(..., min_length=1)
    context: Dict[str, Any] = Field(default_factory=dict)


class BobTestRequest(BaseModel):
    code: str
    test_type: str = "unit"
    context: Dict[str, Any] = Field(default_factory=dict)


class BobChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    workflow_id: str = ""
    context: Dict[str, Any] = Field(default_factory=dict)
