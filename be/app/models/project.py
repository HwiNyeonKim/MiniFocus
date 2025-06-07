"""Project model."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.item import ItemStatus


class Project(Base):
    """Project model."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(
        SQLEnum(ItemStatus), default=ItemStatus.TODO, nullable=False
    )
    is_flagged = Column(Boolean, default=False, nullable=False)
    is_inbox = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Relationships
    action_items = relationship("ActionItem", back_populates="project")
