from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, insert, update

from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models.user import User
from schemas.user import (
    UserCreate,
    UserDeactivate,
    UserLogin,
    UserRead,
)
from database.db import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.config import settings

from datetime import datetime, timedelta
from jose import jwt, JWTError

from .auth_helper import (
    authenticate_user,
    create_access_token,
    oauth2_scheme,
    SECRET_TOKEN,
    ALGORITHM,
    hash_password,
    verify_password,
    get_current_user,
)

from repositories.user import UserRepo

from models.wallet import Wallet

router = APIRouter(prefix="/user", tags=["user"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/")
async def create_user(
    db: Annotated[AsyncSession, Depends(get_db)], create_user: UserCreate
):
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

    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.post("/login")
async def login_user(
    db: Annotated[AsyncSession, Depends(get_db)], user_login: UserLogin
):
    user = await UserRepo().find_by_username(user_login.username, user_login.password)

    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "status_code": status.HTTP_200_OK,
        "message": "Login succesful",
    }


# TODO "соединить" с /login??
@router.post("/token")
async def create_token(
    db: Annotated[AsyncSession, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    token = await create_access_token(
        user.username, user.id, user.is_admin, timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def read_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    stmt = select(User).where(User.username == current_user.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}")
async def deactivate_user_by_id(
    user: UserDeactivate, db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await UserRepo().deactivate_user(user.id)
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "User deactivated successfully",
    }
