from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project as ProjectModel
from app.schemas.project import Project, ProjectCreate, ProjectUpdate

from ..dependencies import get_db

router = APIRouter()


@router.post("/projects/", response_model=Project)
async def create_project(
    project: ProjectCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new project."""
    db_project = ProjectModel(**project.model_dump())
    db.add(db_project)

    await db.commit()
    await db.refresh(db_project)

    return Project.model_validate(db_project)


@router.get("/projects/", response_model=List[Project])
async def get_projects(db: AsyncSession = Depends(get_db)):
    """Get all projects."""
    result = await db.execute(select(ProjectModel))
    projects = result.scalars().all()

    return [Project.model_validate(project) for project in projects]


@router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """Get a project by ID."""
    project = await db.get(ProjectModel, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return Project.model_validate(project)


@router.put("/projects/{project_id}", response_model=Project)
async def update_project(
    project_id: int, project: ProjectUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a project."""
    db_project = await db.get(ProjectModel, project_id)

    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)

    await db.commit()
    await db.refresh(db_project)

    return Project.model_validate(db_project)


@router.delete("/projects/{project_id}", response_model=dict[str, str])
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a project."""
    project = await db.get(ProjectModel, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.is_inbox:
        raise HTTPException(
            status_code=400, detail="Cannot delete Inbox project"
        )

    await db.delete(project)
    await db.commit()

    return {"message": "Project deleted successfully"}
