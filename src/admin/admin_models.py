from sqladmin import ModelView

from models.user import User
from models.wallet import Wallet
from models.transaction import Transaction


class UserAdmin(ModelView, model=User):
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
    ]
