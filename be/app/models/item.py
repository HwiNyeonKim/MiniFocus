"""Action item model."""
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# TODO: 별도 파일로 분리 및 이름 수정. Project에서도 동일한 목적으로 공유하여 사용하는 Enum이다.
class ItemStatus(str, Enum):
    """Item status enum."""

    TODO = "todo"
    DONE = "done"
    DROPPED = "dropped"
    DEFERRED = "deferred"


class ActionItem(Base):
    """Action item model."""

    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        SQLEnum(ItemStatus), default=ItemStatus.TODO, nullable=False
    )
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
