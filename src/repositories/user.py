from utils.repository import SQLAlchemyRepository
from models.user import User

class UserRepo(SQLAlchemyRepository):
    model = User