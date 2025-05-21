from datetime import datetime, timezone
from src.database.models.user import User
from src.dtos.user_dtos import CreateUserDTO, UserDTO, UserLoginDTO
from src.exceptions.user_exceptions import UserConflictError, UserNotFoundError

class UserRepository:

    async def create(self, create_user_dto: CreateUserDTO) -> UserDTO:

        user = await User.find_one(User.email == create_user_dto.email)

        if user:
            raise UserConflictError()
        
        new_user = User(
            name=create_user_dto.name,
            cpf=create_user_dto.cpf,
            telephone=create_user_dto.telephone,
            email=create_user_dto.email,
            password=create_user_dto.password,
            created_at=datetime.now(timezone.utc)
            
        )
        await new_user.insert()

        return UserDTO(
            id=str(new_user.id),
            name=new_user.name,
            telephone=new_user.telephone,
            email=str(new_user.email),
            created_at=str(new_user.created_at)
        )
    
    async def get_user_by_email(self, email: str) -> UserLoginDTO:

        user = await User.find_one(User.email == email)

        if not user:
            raise UserNotFoundError()
        
        return UserLoginDTO(
            email=user.email,
            password_hash=user.password
        )
    
    async def get_by_cpf(self, cpf: str) -> UserDTO:

        user = await User.find_one(User.cpf == cpf)

        if not user:
            raise UserNotFoundError()
        
        return UserDTO(
            id=str(user.id),
            name=user.name,
            telephone=user.telephone,
            email=user.email,
            created_at=str(user.created_at)
        )