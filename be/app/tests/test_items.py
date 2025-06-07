"""Test action item API endpoints."""
import pytest
from httpx import AsyncClient

from app.models import ActionItem, Project


@pytest.mark.asyncio
async def test_create_action_item(client: AsyncClient, test_db):
    """Test creating a new action item."""
    # Create test project
    project = Project(
        name="Test Project", description="Test Description", is_inbox=False
    )
    test_db.add(project)
    await test_db.commit()

    response = await client.post(
        f"/api/projects/{project.id}/items/",
        json={
            "title": "Test Item",
            "description": "This is a test item",
            "due_date": "2024-12-31T23:59:59",
            "is_completed": False,
            "priority": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "This is a test item"
    assert data["is_completed"] is False
    assert data["priority"] == 1
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_action_items(client: AsyncClient, test_db):
    """Test getting all action items for a project."""
    # Create test project and items
    project = Project(
        name="Test Project", description="Test Description", is_inbox=False
    )
    test_db.add(project)
    await test_db.commit()

    item1 = ActionItem(
        title="Item 1",
        description="First item",
        project_id=project.id,
        is_completed=False,
        priority=1,
    )
    item2 = ActionItem(
        title="Item 2",
        description="Second item",
        project_id=project.id,
        is_completed=False,
        priority=2,
    )
    test_db.add(item1)
    test_db.add(item2)
    await test_db.commit()

    response = await client.get(f"/api/projects/{project.id}/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Item 1"
    assert data[1]["title"] == "Item 2"


@pytest.mark.asyncio
async def test_get_action_item(client: AsyncClient, test_db):
    """Test getting a single action item."""
    # Create test project and item
    project = Project(
        name="Test Project", description="Test Description", is_inbox=False
    )
    test_db.add(project)
    await test_db.commit()

    item = ActionItem(
        title="Test Item",
        description="Test description",
        project_id=project.id,
        is_completed=False,
        priority=1,
    )
    test_db.add(item)
    await test_db.commit()

    response = await client.get(f"/api/projects/{project.id}/items/{item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "Test description"


@pytest.mark.asyncio
async def test_update_action_item(client: AsyncClient, test_db):
    """Test updating an action item."""
    # Create test project and item
    project = Project(
        name="Test Project", description="Test Description", is_inbox=False
    )
    test_db.add(project)
    await test_db.commit()

    item = ActionItem(
        title="Original Title",
        description="Original description",
        project_id=project.id,
        is_completed=False,
        priority=1,
    )
    test_db.add(item)
    await test_db.commit()

    response = await client.put(
        f"/api/projects/{project.id}/items/{item.id}",
        json={
            "title": "Updated Title",
            "description": "Updated description",
            "is_completed": True,
            "priority": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"
    assert data["is_completed"] is True
    assert data["priority"] == 2


@pytest.mark.asyncio
async def test_delete_action_item(client: AsyncClient, test_db):
    """Test deleting an action item."""
    # Create test project and item
    project = Project(
        name="Test Project", description="Test Description", is_inbox=False
    )
    test_db.add(project)
    await test_db.commit()

    item = ActionItem(
        title="Test Item",
        description="Test description",
        project_id=project.id,
        is_completed=False,
        priority=1,
    )
    test_db.add(item)
    await test_db.commit()

    response = await client.delete(
        f"/api/projects/{project.id}/items/{item.id}"
    )
    assert response.status_code == 200

    # Verify item is deleted
    response = await client.get(f"/api/projects/{project.id}/items/{item.id}")
    assert response.status_code == 404
