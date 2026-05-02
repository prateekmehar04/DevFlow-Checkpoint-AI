"""Project database model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base

if TYPE_CHECKING:
    from .checkpoint import Checkpoint
    from .workflow import Workflow


class Project(Base):
    """Project model for storing project information."""
    
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tech_stack = Column(JSON, default={})
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    checkpoints = relationship(
        "Checkpoint",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    workflows = relationship(
        "Workflow",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name={self.name})>"

# Made with Bob
