from datetime import timedelta
from http.client import HTTPException
import os
from server.api.schemas.auth import Oauth
from server.database.main import get_db
from server.config import jwt_settings
from server.helpers.auth.main import create_access_token
from fastapi import APIRouter
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.requests import Request
from starlette.responses import RedirectResponse

google_router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

BACKEND_URL = os.getenv("BACKEND_URL")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = f"{BACKEND_URL}/auth/google/callback"
FRONTEND_URL = os.getenv("FRONTEND_URL")

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={"scope": "email openid profile", "redirect_url": GOOGLE_REDIRECT_URI},
)


@google_router.get("/google")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)


@google_router.get("/google/callback")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)

    except OAuthError as e:
        print(f"OAuth Error: {e.error}")
        print(f"Description: {e.description}")
        return RedirectResponse(url="/error")  # Redirect to an error page

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info")

    # Extract relevant information from user_info
    email = user_info.get("email")
    # Check if user exists in the database
    redirect_url = f"{FRONTEND_URL}/auth/verify?token={token}&email={email}"

    with get_db() as db:
        # check if email is in db
        user = db.query(Oauth).filter(Oauth.email == email).first()

        access_token_expires = timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(data={"sub": email}, expires_delta=access_token_expires)

        if not user:
            # register the user
            new_user = Oauth(email = email,profilePic = user_info.get("picture"))
            
            db.add(new_user)
           
            db.commit()
            

        return RedirectResponse(url = redirect_url)
