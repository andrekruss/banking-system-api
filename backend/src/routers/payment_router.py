from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from src.database.models.payment import PaymentType
from src.database.models.user import User
from src.database.repositories.account_repository import AccountRepository
from src.database.repositories.payment_repository import PaymentRepository
from src.database.repositories.user_repository import UserRepository
from src.dtos.payment_dtos import CreatePaymentDTO, PaymentDTO
from src.utils.authenticate_user import get_current_user

payment_router = APIRouter(prefix="/payments", tags=["payments"])

# @payment_router.post(path="/create", status_code=status.HTTP_201_CREATED, response_model=PaymentDTO)
# async def create_payment(create_payment_dto: CreatePaymentDTO, user: User = Depends(get_current_user)):
    
#     try:
#         # Find payment's source account
#         account_repo = AccountRepository()
#         account = await account_repo.get_by_user_id(user.id)

#         # If payment is PIX, find target account
#         if create_payment_dto.payment_type == PaymentType.PIX:
#             user_repo = UserRepository()
#             target_user = await User.get_by_cpf(create_payment_dto.target_identifier)
#             target_account = await account_repo.get_by_user_id(PydanticObjectId(target_user.id))

#             if account.balance < create_payment_dto.amount:     