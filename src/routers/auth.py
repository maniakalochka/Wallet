from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache.decorator import cache
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from models.user import User
from models.wallet import Wallet
from repositories.user import UserRepo
from schemas.user import SuperUserCreate, UserCreate, UserDeactivate, UserRead

from .auth_helper import (authenticate_user, create_access_token,
                          get_current_user, hash_password)

auth_router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_router.post("/")
async def create_user(
    db: Annotated[AsyncSession, Depends(get_db)], create_user: UserCreate
):
    """
    Create a new user, and a wallet for the user
    """
    user_dict = create_user.model_dump()
    existing_user = await UserRepo().check_exists(
        username=create_user.username, email=create_user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User or email already exists",
        )
    user_dict["hashed_password"] = hash_password(user_dict["hashed_password"])

    new_user = await UserRepo().add_one(user_dict)

    new_wallet = Wallet(user_id=new_user.id)
    async with db.begin():
        db.add(new_wallet)

    return {"status_code": status.HTTP_201_CREATED, "msg": "Successful"}


@auth_router.post("/mkadmin")
async def create_admin(
    db: Annotated[AsyncSession, Depends(get_db)], create_superuser: SuperUserCreate
):
    """
    create a superuser, and DON'T create wallet
    """
    user_dict = create_superuser.model_dump()
    existing_user = await UserRepo().check_exists(
        username=create_superuser.username, email=create_superuser.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User or email already exists",
        )
    user_dict["hashed_password"] = hash_password(user_dict["hashed_password"])
    user_dict["is_admin"] = True

    await UserRepo().add_one(user_dict)

    return {"status_code": status.HTTP_201_CREATED, "msg": "Successful"}


@auth_router.post("/login")
async def login(
    db: Annotated[AsyncSession, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    Login a user, and return an access token
    """
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password, or user is inactive",
        )
    access_token_expires = timedelta(minutes=20)
    token = create_access_token(
        data={"id": user.id, "username": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires,
    )

    return {
        "status_code": status.HTTP_200_OK,
        "access_token": token,
        "token_type": "bearer",
    }


@auth_router.get("/me", response_model=UserRead)
@cache(expire=60)
async def read_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Return the current user
    """
    user = await UserRepo().find_by_username(current_user.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@auth_router.patch("/{user_id}")
async def deactivate_user_by_id(
    user: UserDeactivate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Ban a user by id (Only admin can do this)
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    user = await UserRepo().deactivate_user(user.id)
    return {
        "status_code": status.HTTP_200_OK,
        "msg": "User deactivated successfully",
    }
