from utils.repository import SQLAlchemyRepository
from models.transaction import Transaction


class TransactionRepo(SQLAlchemyRepository):
    model = Transaction
