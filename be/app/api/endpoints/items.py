"""Action item endpoints."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.item import ActionItem as ActionItemModel
from app.models.project import Project
from app.schemas.item import ActionItem, ActionItemCreate, ActionItemUpdate

router = APIRouter()


@router.get("/projects/{project_id}/items/", response_model=List[ActionItem])
async def list_action_items(
    project_id: int, db: AsyncSession = Depends(get_db)
):
    """List all action items for a project."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Query action items directly instead of accessing through relationship
    items = await db.execute(
        select(ActionItemModel).where(ActionItemModel.project_id == project_id)
    )
    items = items.scalars().all()
    return [ActionItem.model_validate(item) for item in items]


@router.post("/projects/{project_id}/items/", response_model=ActionItem)
async def create_action_item(
    project_id: int, item: ActionItemCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new action item for a project."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_item = ActionItemModel(**item.model_dump())
    db_item.project_id = project_id
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return ActionItem.model_validate(db_item)


@router.get(
    "/projects/{project_id}/items/{item_id}", response_model=ActionItem
)
async def get_action_item(
    project_id: int, item_id: int, db: AsyncSession = Depends(get_db)
):
    """Get a specific action item for a project."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    item = await db.get(ActionItemModel, item_id)
    if not item or item.project_id != project_id:
        raise HTTPException(status_code=404, detail="Action item not found")
    return ActionItem.model_validate(item)


@router.put(
    "/projects/{project_id}/items/{item_id}", response_model=ActionItem
)
async def update_action_item(
    project_id: int,
    item_id: int,
    item: ActionItemUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a specific action item for a project."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_item = await db.get(ActionItemModel, item_id)
    if not db_item or db_item.project_id != project_id:
        raise HTTPException(status_code=404, detail="Action item not found")
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return ActionItem.model_validate(db_item)


@router.delete(
    "/projects/{project_id}/items/{item_id}", response_model=dict[str, str]
)
async def delete_action_item(
    project_id: int, item_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete an action item."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_item = await db.get(ActionItemModel, item_id)
    if not db_item or db_item.project_id != project_id:
        raise HTTPException(status_code=404, detail="Action item not found")
    await db.delete(db_item)
    await db.commit()
    return {"message": "Action item deleted successfully"}
