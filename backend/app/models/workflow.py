"""Workflow database model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base

if TYPE_CHECKING:
    from .project import Project


class Workflow(Base):
    """Workflow model for storing workflow state and history."""
    
    __tablename__ = "workflows"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    current_state = Column(String(50), nullable=False, default="plan")
    context = Column(JSON, nullable=False, default={})
    state_history = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="workflows")
    
    # Indexes
    __table_args__ = (
        Index('idx_workflows_project', 'project_id'),
        Index('idx_workflows_state', 'current_state'),
    )
    
    def __repr__(self) -> str:
        return f"<Workflow(id={self.id}, state={self.current_state})>"

# Made with Bob
