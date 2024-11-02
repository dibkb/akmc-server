from fastapi import FastAPI
from server.api.endpoints import base_router
import uvicorn
import os
from server.database.main import init_db

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
app = FastAPI()

@app.get("/test")
async def read_root():
    return {"Hello": "World "}

# routers
app.include_router(base_router)
init_db()
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        log_level="debug",
        reload=True,
    )
