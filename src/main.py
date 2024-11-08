from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to Wallet"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, reload=True)
