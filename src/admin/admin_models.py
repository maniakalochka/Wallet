from datetime import timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import RedirectResponse

from core.config import settings
from models.transaction import Transaction
from models.user import User
from models.wallet import Wallet
from repositories.user import UserRepo
from routers.auth_helper import (authenticate_user, create_access_token,
                                 get_current_user, verify_password)

SECRET_TOKEN = settings.SECRET_TOKEN
ALGORITHM = "HS256"


class UserAdmin(ModelView, model=User):
    def date_format(value):
        return value.strftime("%d.%m.%Y")

    name = "Пользователь"
    name_plural = "Пользователи"
    category = "Пользователи"
    column_list = [
        "id",
        "username",
        "email",
        "is_active",
        "is_superuser",
        "created_date",
        "wallet",
        "transactions",
    ]
    column_searchable_list = ["username", "email"]
    column_sortable_list = ["id", "username", "email", "created_date"]
    form_edit_rules = ["is_active", "username"]
    column_export_exclude_list = ["password", "is_superuser"]
    can_view_details = False


class WalletAdmin(ModelView, model=Wallet):
    def date_format(value):
        return value.strftime("%d.%m.%Y")

    name = "Кошелек"
    name_plural = "Кошельки"
    category = "Кошельки"
    column_list = ["id", "balance", "user", "transactions"]
    column_sortable_list = ["id", "balance", "user"]
    column_searchable_list = ["user.username"]
    form_edit_rules = ["balance", "user"]


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        db = request.state.db
        user = await authenticate_user(db, username, password)
        print(user)
        if not user or not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password, or user is not admin",
            )
        token = create_access_token(
            data={"id": user.id, "username": user.username, "is_admin": user.is_admin},
            expires_delta=timedelta(minutes=30),
        )
        request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        db = request.state.db
        user = await get_current_user(token, db)
        if user:
            return True
        if not user:
            return False


authentication_backend = AdminAuth(secret_key=SECRET_TOKEN)
