from fastapi import FastAPI
from core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
)


@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to Wallet"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000, reload=True)
