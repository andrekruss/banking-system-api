from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from src.database.models.payment import PaymentType
from src.database.models.user import User
from src.database.repositories.account_repository import AccountRepository
from src.database.repositories.payment_repository import PaymentRepository
from src.database.repositories.user_repository import UserRepository
from src.dtos.payment_dtos import CreatePaymentDTO, PaymentDTO
from src.exceptions.account_exceptions import AccountNotFoundError
from src.utils.authenticate_user import get_current_user

payment_router = APIRouter(prefix="/payments", tags=["payments"])

@payment_router.post(path="/create", status_code=status.HTTP_201_CREATED, response_model=PaymentDTO)
async def create_payment(create_payment_dto: CreatePaymentDTO, user: User = Depends(get_current_user)):
    
    try:
        # Find payment's source account
        account_repo = AccountRepository()
        account = await account_repo.get_by_user_id(user.id)

        # Verify if  source account has enough funds
        if account.balance < create_payment_dto.amount: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough funds to realize payment."
            )

        # Create payment
        payment_repo = PaymentRepository()
        payment_dto = await payment_repo.create(
            user.id,
            account.id,
            create_payment_dto
        )

        # If payment is PIX, find target account and update balance
        if create_payment_dto.payment_type.value == PaymentType.PIX:
            user_repo = UserRepository()
            target_user = await user_repo.get_by_cpf(create_payment_dto.target_identifier)
            target_account = await account_repo.get_by_user_id(PydanticObjectId(target_user.id))
            updated_balance = target_account.balance + create_payment_dto.amount
            await account_repo.update_balance(PydanticObjectId(target_account.id), updated_balance)

        # Update source account balance
        await account_repo.update_balance(PydanticObjectId(account.id), account.balance - create_payment_dto.amount)

        return payment_dto     
    except AccountNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        ) 
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )