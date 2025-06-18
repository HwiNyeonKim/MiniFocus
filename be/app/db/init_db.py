from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.user import User

from .session import Base, engine


async def init_db():
    """Initialize database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_inbox_project(db: AsyncSession):
    """Create inbox project if it doesn't exist."""
    # Create default user if not exists
    result = await db.execute(select(User).filter(User.email == "admin@example.com"))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            email="admin@example.com",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
            is_active=True,
            is_superuser=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    # Create inbox project if not exists
    result = await db.execute(select(Project).filter(Project.name == "Inbox"))
    inbox = result.scalar_one_or_none()

    if not inbox:
        inbox = Project(
            name="Inbox",
            description="Default inbox project",
            is_inbox=True,
            owner_id=user.id
        )
        db.add(inbox)

        await db.commit()
