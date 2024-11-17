from utils.repository import SQLAlchemyRepository
from models.wallet import Wallet


class WalletRepo(SQLAlchemyRepository):
    model = Wallet
