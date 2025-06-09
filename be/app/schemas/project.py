from pydantic import BaseModel


class ProjectBase(BaseModel):
    """Base Project schema."""

    name: str
    description: str | None = None
    is_inbox: bool = False
    parent_id: int | None = None


class ProjectCreate(ProjectBase):
    """Project creation schema."""

    pass


class ProjectUpdate(BaseModel):
    """Project update schema."""

    name: str | None = None
    description: str | None = None
    is_inbox: bool | None = None


class Project(ProjectBase):
    """Project response schema."""

    id: int

    class Config:
        """Pydantic config."""

        from_attributes = True
