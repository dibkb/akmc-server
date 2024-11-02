from fastapi import FastAPI
import uvicorn

from server.database.main import init_db
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World "}


init_db()
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        reload=True,
    )
