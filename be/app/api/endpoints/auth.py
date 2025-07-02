from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.core import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.models import User as UserModel, Project as ProjectModel
from app.schemas import User, UserCreate, UserUpdate

router = APIRouter()


@router.post("/register", response_model=User)
async def register(*, db: AsyncSession = Depends(get_db), user_in: UserCreate):
    """Register new user."""
    # Check if user exists
    result = await db.execute(
        select(UserModel).filter(UserModel.email == user_in.email)
    )
    user = result.scalar_one_or_none()

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    # Create new user
    user = UserModel(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Create Inbox project for the new user
    inbox_project = ProjectModel(
        name="Inbox",
        description="Default inbox project for unassigned tasks",
        is_inbox=True,
        owner_id=user.id,
    )
    db.add(inbox_project)
    await db.commit()

    return user


@router.post("/login")
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    result = await db.execute(
        select(UserModel).filter(UserModel.email == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh access token."""

    return {
        "access_token": create_access_token(current_user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user."""

    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update own user."""
    if user_in.password is not None:
        current_user.hashed_password = get_password_hash(user_in.password)

    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name

    if user_in.email is not None:
        current_user.email = user_in.email

    await db.commit()
    await db.refresh(current_user)

    return current_user
