from datetime import timedelta,datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from jose import jwt

from server.api.models.auth import TokenData
from server.api.schemas.auth import User
from server.config import jwt_settings
def get_user(db: Session, email: str) -> User:
    """Retrieve a user by their username."""
    existing_user = db.query(User).filter(User.email == email).first()

    # If the user is found, return it
    if existing_user:
        return existing_user

    # If the user is not found, raise an exception
    if existing_user is None:
        raise HTTPException(status_code=400, detail="Username does not exist")
    


def create_access_token(data: TokenData, expires_delta: timedelta | None = None) -> str:
    """

    """
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=120)

    # Update the data with the expiration time
    data.update({"exp": expire})

    # Encode the data as a JWT using the secret key and the specified algorithm
    encoded_jwt = jwt.encode(data, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)

    return encoded_jwt    