from fastapi import FastAPI, APIRouter
from core.config import settings
from routers import auth, wallet, transaction


app = FastAPI(
    title=settings.APP_NAME,
)


app.include_router(auth.auth_router, tags=["user"])
app.include_router(wallet.wallet_router, tags=["wallet"])
app.include_router(transaction.transaction_router, tags=["transaction"])


@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to Wallet"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000, reload=True)
