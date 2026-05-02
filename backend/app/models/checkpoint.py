"""Checkpoint database model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base

if TYPE_CHECKING:
    from .project import Project
    from .user import User


class Checkpoint(Base):
    """Checkpoint model for storing project snapshots."""
    
    __tablename__ = "checkpoints"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    milestone = Column(String(50), nullable=False)
    state_data = Column(JSON, nullable=False, default={})
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="checkpoints")
    
    # Indexes
    __table_args__ = (
        Index('idx_checkpoints_project', 'project_id'),
        Index('idx_checkpoints_milestone', 'milestone'),
        Index('idx_checkpoints_created_at', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<Checkpoint(id={self.id}, milestone={self.milestone})>"

# Made with Bob
