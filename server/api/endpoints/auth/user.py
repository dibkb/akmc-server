from fastapi import APIRouter,HTTPException
from server.database.main import get_db
from server.helpers.auth.main import get_user
from fastapi.encoders import jsonable_encoder


user_router = APIRouter(
    prefix="/user",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/{email}", response_model=dict)
def register_user(email: str) -> dict:
    """
    Register a new user.
    """
    with get_db() as db:
        try:

            user = get_user(db,email = email)

            if not user:
                raise HTTPException(
                    status_code=404,
                    detail=f"User with email {email} not found"
            )

            return jsonable_encoder(user)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
