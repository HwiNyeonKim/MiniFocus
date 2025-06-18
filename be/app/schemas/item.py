from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.item import ItemStatus


# TODO: project 내용이 섞여 있다. Task 관련 내용만 남기기
class ProjectBase(BaseModel):
    """Base Project schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: ItemStatus = ItemStatus.TODO
    is_flagged: bool = False
    parent_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    """Project creation schema."""

    pass


class ProjectUpdate(ProjectBase):
    """Project update schema."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)


class ProjectInDB(ProjectBase):
    """Project database schema."""

    id: int
    is_inbox: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class Project(ProjectInDB):
    """Project response schema."""

    subprojects: List["Project"] = []
    action_items: List["ActionItem"] = []


class ActionItemBase(BaseModel):
    """Base ActionItem schema."""

    title: str
    description: str | None = None
    status: ItemStatus = ItemStatus.TODO
    is_flagged: bool = False
    due_date: datetime | None = None
    priority: int = 0


class ActionItemCreate(ActionItemBase):
    """ActionItem creation schema."""

    pass


class ActionItemUpdate(BaseModel):
    """ActionItem update schema."""

    title: str | None = None
    description: str | None = None
    status: ItemStatus | None = None
    is_flagged: bool | None = None
    due_date: datetime | None = None
    priority: int | None = None


class ActionItem(ActionItemBase):
    """ActionItem response schema."""

    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


# Update forward references
Project.model_rebuild()
ActionItem.model_rebuild()
