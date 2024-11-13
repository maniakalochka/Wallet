from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, insert

from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models.user import User
from schemas.user import UserCreate, SuperUserCreate
from database.db import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.config import settings

from datetime import datetime, timedelta
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(prefix='/auth', tags=['auth'])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_TOKEN = settings.SECRET_TOKEN
ALGORITHM = 'HS256'

@router.post('/')
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], create_user: UserCreate):
    existing_user = await db.scalar(select(User).where((User.username == create_user.username) | (User.email == create_user.email)))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User or email already exists'
        )
    await db.execute(insert(User).values(first_name=create_user.first_name,
                                         last_name=create_user.last_name,
                                         username=create_user.username,
                                         email=create_user.email,
                                         hashed_password=bcrypt_context.hash(create_user.password),
                                         ))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.post('/superuser')
async def create_superuser(superuser: SuperUserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    existing_user = await db.scalar(select(User).where((User.username == superuser.username) | (User.email == superuser.email)))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User or email already exists'
        )
    await db.execute(insert(User).values(first_name=superuser.first_name,
                                         last_name=superuser.last_name,
                                         username=superuser.username,
                                         email=superuser.email,
                                         hashed_password=bcrypt_context.hash(superuser.password),
                                         is_admin=superuser.is_admin
                                         ))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.post('/token')
async def login(db: Annotated[AsyncSession, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )

    token = await create_access_token(user.username, user.id, user.is_admin, timedelta(minutes=20))

    return {
        'access_token': token,
        'token_type': 'bearer'
    }

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     try:
#         payload = jwt.decode(token, SECRET_TOKEN, algorithms=[ALGORITHM])
#         username: str = payload.get('sub')
#         user_id: int = payload.get('id')
#         is_admin: str = payload.get('is_admin')
#         expire = payload.get('exp')
#         if username is None or user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail='Could not validate user'
#             )
#         if expire is None:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="No access token supplied"
#             )
#         if datetime.now() > datetime.fromtimestamp(expire):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Token expired!"
#             )

#         return {
#             'username': username,
#             'id': user_id,
#             'is_admin': is_admin,
#         }
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Could not validate user'
#         )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        payload = jwt.decode(token, SECRET_TOKEN, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        user = await db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")

@router.get("/read_current_user")
async def read_current_user(user: User = Depends(oauth2_scheme)):
    return user


async def authenticate_user(db: Annotated[AsyncSession, Depends(get_db)], username: str, password: str):
    user = await db.scalar(select(User).where(User.username == username))
    if not user or not bcrypt_context.verify(password, user.hashed_password) or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def create_access_token(username: str, user_id: int, is_admin: bool, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'is_admin': is_admin}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_TOKEN, algorithm=ALGORITHM)

