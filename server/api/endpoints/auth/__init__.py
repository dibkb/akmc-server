from fastapi import APIRouter
from server.api.endpoints.auth.register import register_router
from server.api.endpoints.auth.login import login_router
from server.api.endpoints.auth.google import google_router
from server.api.endpoints.auth.user import user_router
auth_router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"description": "Not found"}})

auth_router.include_router(register_router)
auth_router.include_router(login_router)
auth_router.include_router(google_router)
auth_router.include_router(user_router)
