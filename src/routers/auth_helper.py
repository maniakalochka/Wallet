from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, HTTPException
from auth import oauth2_scheme
from database.db import get_db
from auth import bcrypt_context, SECRET_TOKEN, ALGORITHM
from jose import jwt, JWTError
from sqlalchemy import select
from models import User
from datetime import datetime, timedelta


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
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


async def authenticate_user(
    db: Annotated[AsyncSession, Depends(get_db)], username: str, password: str
):
    user = await db.scalar(select(User).where(User.username == username))
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


async def create_access_token(
    username: str, user_id: int, is_admin: bool, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "is_admin": is_admin}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_TOKEN, algorithm=ALGORITHM)