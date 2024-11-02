from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    sub: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int | None = None    