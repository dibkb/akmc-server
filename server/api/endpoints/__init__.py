from fastapi import APIRouter
from server.api.endpoints.auth import auth_router

base_router = APIRouter(responses={404: {"description": "Not found"}})

base_router.include_router(auth_router)
