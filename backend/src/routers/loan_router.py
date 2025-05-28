from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from src.database.repositories.account_repository import AccountRepository
from src.database.repositories.loan_repository import LoanRepository
from src.database.models.user import User
from src.dtos.loan_dtos import CreateLoanDTO, LoanDTO
from src.exceptions.account_exceptions import AccountNotFoundError
from src.utils.authenticate_user import get_current_user

loan_router = APIRouter(prefix="/loans", tags=["loans"])

@loan_router.post(path="/create", status_code=status.HTTP_201_CREATED, response_model=LoanDTO)
async def create_loan(create_loan_dto: CreateLoanDTO, user: User = Depends(get_current_user)):

    try:
        account_repo = AccountRepository()

        account_dto = await account_repo.get_by_user_id(user.id)

        loan_repo = LoanRepository()

        total = create_loan_dto.amount * (1 + create_loan_dto.interest_rate)
        installment_amount = total / create_loan_dto.installments

        loan_dto = await loan_repo.create(
            user_id=user.id,
            account_id=PydanticObjectId(account_dto.id),
            total=total,
            installment_amount=installment_amount,
            create_loan_dto=create_loan_dto
        )

        await account_repo.update_balance(PydanticObjectId(account_dto.id), account_dto.balance + loan_dto.amount)

        return loan_dto

    except AccountNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
    