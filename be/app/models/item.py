"""Action item model."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.status import Status


class ActionItem(Base):
    """Action item model."""

    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(Status), default=Status.TODO, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)
    due_date = Column(DateTime, nullable=True)
    priority = Column(Integer, default=0, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False,
    )

    project = relationship("Project", back_populates="action_items")
