from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, HTTPException
from database.db import get_db
from jose import jwt, JWTError
from models.user import User
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from passlib.context import CryptContext
from repositories.user import UserRepo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_TOKEN = settings.SECRET_TOKEN
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Get the current user from the token (Used in Depends())
    """
    try:
        payload = jwt.decode(token, SECRET_TOKEN, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        user = await db.get(User, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


async def authenticate_user(db: AsyncSession, username: str, password: str):
    """
    Authenticate the user using the username and password
    """
    user = await UserRepo().find_by_username(username)
    if (
        not user
        or not bcrypt_context.verify(password, user.hashed_password)
        or user.is_active == False
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(data: dict, expires_delta: timedelta):
    """
    Create an access token for the user
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt
