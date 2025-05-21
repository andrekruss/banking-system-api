from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from src.database.repositories.account_repository import AccountRepository
from src.database.repositories.user_repository import UserRepository
from src.dtos.account_dtos import CreateAccountDTO
from src.dtos.user_dtos import CreateUserDTO, UserDTO
from src.exceptions.user_exceptions import UserConflictError
from src.utils.hash import hash_password

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post(path="/register", status_code=status.HTTP_201_CREATED, response_model=UserDTO)
async def register_user(create_user_dto: CreateUserDTO):

    try:
        user_repo = UserRepository()
        create_user_dto.password = hash_password(create_user_dto.password)
        user = await user_repo.create(create_user_dto)

        account_repo = AccountRepository()
        account = await account_repo.create(
            CreateAccountDTO(
                user_id=PydanticObjectId(user.id),
                balance=0
            )
        )

        return user
    except UserConflictError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

    