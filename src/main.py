import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis
from redis import asyncio as aioredis
from sqladmin import Admin, ModelView

from admin.admin_models import (
    AdminAuth,
    UserAdmin,
    WalletAdmin,
    authentication_backend,
    TransactionAdmin,
)
from core.config import Settings, settings
from database.db import engine, init_db
from middleware.middlewares import DBSessionMiddleware
from models.user import User
from routers import auth, transaction, wallet
from logger import logger

SECRET_TOKEN = settings.SECRET_TOKEN


app = FastAPI(
    title=settings.APP_NAME,
)

app.add_middleware(DBSessionMiddleware)

authentication_backend = AdminAuth(secret_key=SECRET_TOKEN)
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(WalletAdmin)
admin.add_view(TransactionAdmin)


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


@app.middleware("http")
async def add_log(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={"time": round(process_time, 4)})
    return response


if __name__ == "__main__":
    import uvicorn

    init_db()
    uvicorn.run(app=app, host="localhost", port=8000, reload=True)
