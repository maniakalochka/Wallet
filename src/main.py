from fastapi import FastAPI, APIRouter
from core.config import settings
from routers import auth



app = FastAPI(
    title=settings.APP_NAME,
)



app.include_router(auth.router, tags=["auth"])

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to Wallet"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000, reload=True)
