from pydantic import BaseModel
import os
class Settings(BaseModel):
    DB_HOST: str = os.getenv("DB_HOST", "localhost")

    DB_NAME: str = os.getenv("DB_NAME", "my_app")
    DB_USER: str = os.getenv("DB_USER", "my_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "my_password")
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


settings = Settings()


class JWTSettings(BaseModel):
    SECRET_KEY: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE"))


jwt_settings = JWTSettings()