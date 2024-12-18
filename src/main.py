from fastapi import FastAPI
from core.config import settings
from routers import auth, wallet, transaction
from core.config import Settings
from database.db import init_db

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis


app = FastAPI(
    title=settings.APP_NAME,
)


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
