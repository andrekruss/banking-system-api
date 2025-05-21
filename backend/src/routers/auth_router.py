from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.exceptions.user_exceptions import UserNotFoundError
from src.database.repositories.user_repository import UserRepository
from src.dtos.auth_dtos import TokenDTO
from src.utils.hash import verify_password
from src.utils.jwt import generate_jwt_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post(path="/token", status_code=status.HTTP_200_OK, response_model=TokenDTO)
async def login(login_form_data: OAuth2PasswordRequestForm = Depends()):

    try:
        user_repo = UserRepository()

        user_login = await user_repo.get_user_by_email(login_form_data.username)

        if not verify_password(login_form_data.password, user_login.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect user or password.")
        
        jwt_token = generate_jwt_token({"sub": user_login.email})
        return TokenDTO(access_token=jwt_token, token_type="bearer")
    except UserNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )