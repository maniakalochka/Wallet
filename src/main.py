from fastapi import FastAPI
from core.config import settings
from routers import auth, wallet, transaction
from core.config import Settings
from database.db import init_db, engine
from models.user import User

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis
from sqladmin import Admin, ModelView
from admin.admin_models import UserAdmin, WalletAdmin, AdminAuth, authentication_backend
from core.config import settings
from middleware.middlewares import DBSessionMiddleware

SECRET_TOKEN = settings.SECRET_TOKEN


app = FastAPI(
    title=settings.APP_NAME,
)

app.add_middleware(DBSessionMiddleware)

authentication_backend = AdminAuth(secret_key=SECRET_TOKEN)
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(WalletAdmin)


@app.on_event("startup")
async def startup():
    redis = Redis(host="localhost", port=6379, db=0)
    cache = RedisBackend(redis)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


app.include_router(auth.auth_router, tags=["auth"])
app.include_router(wallet.wallet_router, tags=["wallet"])
app.include_router(transaction.transaction_router, tags=["transaction"])


@app.get("/")
async def welcome() -> dict:
    """
    Start page
    """
    return {"message": "Welcome to Wallet"}


if __name__ == "__main__":
    import uvicorn

    init_db()
    uvicorn.run(app=app, host="localhost", port=8000, reload=True)
