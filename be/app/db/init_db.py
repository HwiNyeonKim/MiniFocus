from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project

from .session import Base, engine


async def init_db():
    """Initialize database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_inbox_project(db: AsyncSession):
    """Create inbox project if it doesn't exist."""
    result = await db.execute(select(Project).filter(Project.name == "Inbox"))
    inbox = result.scalar_one_or_none()

    if not inbox:
        inbox = Project(
            name="Inbox", description="Default inbox project", is_inbox=True
        )
        db.add(inbox)

        await db.commit()
