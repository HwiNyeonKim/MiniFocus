"""Import all models here for Alembic to detect them."""
from app.db.base_class import Base  # noqa
from app.models.item import ActionItem  # noqa
from app.models.project import Project  # noqa
