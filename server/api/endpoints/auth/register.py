from datetime import datetime
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from server.api.models.auth import UserCreate
from server.api.schemas.auth import User
from server.database.main import get_db



register_router = APIRouter(
    prefix="/register",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@register_router.post("", response_model=dict)
def register_user(user: UserCreate) -> dict:
    """
    Register a new user.
    """
    with get_db() as db:
        try:
            if db.query(User).filter(User.email == user.email).first():
                raise HTTPException(status_code=400, detail="Email already registered")

            new_user = User(email=user.email)
            new_user.set_password(user.password)
            
            db.add(new_user)
            # Commit changes to the database
            db.commit()

        
            return {
                "msg": "User registered successfully",
                "user_id": new_user.id,
                "email" : new_user.email
            }

        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Database integrity error: {str(e)}")

        except HTTPException:
            db.rollback()
            raise  # Re-raise HTTP exceptions

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
