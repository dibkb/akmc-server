from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from server.api.models.auth import Token, UserCreate
from server.api.schemas.auth import User
from server.database.main import get_db
from server.helpers.auth.main import create_access_token, get_user
from server.config import jwt_settings


login_router = APIRouter(
    prefix="/login",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@login_router.post("", response_model=Token)
def register_user(data: UserCreate) -> Token:
    """
    Register a new user.
    """
    with get_db() as db:
        try:
            user = get_user(db, email=data.email)

            if user.verify_password(data.password):
                access_token_expires = timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)

                token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
                
                return Token(access_token=token, token_type="bearer")
            
            else:
                raise HTTPException(status_code=403, detail=f"Incorrect Password")
            
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Database integrity error: {str(e)}")

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
