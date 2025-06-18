"""Test action item API endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import ActionItem
from app.models.project import Project
from app.models.status import Status


@pytest.mark.asyncio
async def test_create_project(
    client: AsyncClient, test_db: AsyncSession
) -> None:
    """Test creating a project."""
    response = await client.post(
        "/api/v1/projects/",
        json={"name": "Test Project", "description": "Test Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "Test Description"
    assert data["is_inbox"] is False


@pytest.mark.asyncio
async def test_create_action_item(
    client: AsyncClient,
    test_db: AsyncSession,
) -> None:
    """Test creating an action item."""
    # Create a project first
    project = Project(
        name="Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    response = await client.post(
        f"/api/v1/projects/{project.id}/items/",
        json={
            "title": "Test Item",
            "description": "Test Description",
            "status": "todo",
            "priority": 0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "Test Description"
    assert data["status"] == "todo"
    assert data["priority"] == 0
    assert data["project_id"] == project.id


@pytest.mark.asyncio
async def test_list_action_items(
    client: AsyncClient,
    test_db: AsyncSession,
) -> None:
    """Test listing action items."""
    # Create a project first
    project = Project(
        name="Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    # Create some action items
    items = [
        ActionItem(
            title=f"Test Item {i}",
            description=f"Test Description {i}",
            status=Status.TODO,
            priority=i,
            project_id=project.id,
        )
        for i in range(3)
    ]
    test_db.add_all(items)
    await test_db.commit()

    response = await client.get(f"/api/v1/projects/{project.id}/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for i, item in enumerate(data):
        assert item["title"] == f"Test Item {i}"
        assert item["description"] == f"Test Description {i}"
        assert item["status"] == "todo"
        assert item["priority"] == i
        assert item["project_id"] == project.id


@pytest.mark.asyncio
async def test_get_action_item(
    client: AsyncClient,
    test_db: AsyncSession,
) -> None:
    """Test getting an action item."""
    # Create a project first
    project = Project(
        name="Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    # Create an action item
    item = ActionItem(
        title="Test Item",
        description="Test Description",
        status=Status.TODO,
        priority=0,
        project_id=project.id,
    )
    test_db.add(item)
    await test_db.commit()
    await test_db.refresh(item)

    response = await client.get(
        f"/api/v1/projects/{project.id}/items/{item.id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "Test Description"
    assert data["status"] == "todo"
    assert data["priority"] == 0
    assert data["project_id"] == project.id


@pytest.mark.asyncio
async def test_update_action_item(
    client: AsyncClient,
    test_db: AsyncSession,
) -> None:
    """Test updating an action item."""
    # Create a project first
    project = Project(
        name="Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    # Create an action item
    item = ActionItem(
        title="Test Item",
        description="Test Description",
        status=Status.TODO,
        priority=0,
        project_id=project.id,
    )
    test_db.add(item)
    await test_db.commit()
    await test_db.refresh(item)

    response = await client.put(
        f"/api/v1/projects/{project.id}/items/{item.id}",
        json={
            "title": "Updated Item",
            "description": "Updated Description",
            "status": "done",
            "priority": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Item"
    assert data["description"] == "Updated Description"
    assert data["status"] == "done"
    assert data["priority"] == 1
    assert data["project_id"] == project.id


@pytest.mark.asyncio
async def test_delete_action_item(
    client: AsyncClient,
    test_db: AsyncSession,
) -> None:
    """Test deleting an action item."""
    # Create a project first
    project = Project(
        name="Test Project",
        description="Test Description",
        is_inbox=False,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)

    # Create an action item
    item = ActionItem(
        title="Test Item",
        description="Test Description",
        status=Status.TODO,
        priority=0,
        project_id=project.id,
    )
    test_db.add(item)
    await test_db.commit()
    await test_db.refresh(item)

    response = await client.delete(
        f"/api/v1/projects/{project.id}/items/{item.id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Action item deleted successfully"

    # Verify the item is deleted
    response = await client.get(
        f"/api/v1/projects/{project.id}/items/{item.id}",
    )
    assert response.status_code == 404
