from typing import List
from beanie import PydanticObjectId

from src.database.models.loan import Loan
from src.dtos.loan_dtos import CreateLoanDTO, LoanDTO

class LoanRepository:

    async def create(self, user_id:PydanticObjectId,  account_id: PydanticObjectId, total: float, installment_amount: float, create_loan_dto: CreateLoanDTO) -> LoanDTO:


        loan = Loan(
            user_id=user_id,
            account_id=account_id,
            amount=create_loan_dto.amount,
            interest_rate=create_loan_dto.interest_rate,
            installments=create_loan_dto.installments,
            installment_amount=installment_amount,
            outstanding_balance=total,
            due_date=create_loan_dto.due_date
        )

        await loan.insert()

        return LoanDTO(
            id=str(loan.id),
            amount=loan.amount,
            interest_rate=loan.interest_rate,
            installments=loan.installments,
            installment_amount=loan.installment_amount,
            outstanding_balance=loan.outstanding_balance,
            status=loan.status,
            created_at=str(loan.created_at),
            due_date=str(loan.due_date)
        )
    
    async def list_by_user(self, user_id: PydanticObjectId) -> List[LoanDTO]:
        
        loans = await Loan.find(Loan.user_id == user_id).to_list()

        return [
            LoanDTO(
                id=str(loan.id),
                amount=loan.amount,
                interest_rate=loan.interest_rate,
                installments=loan.installments,
                installment_amount=loan.installment_amount,
                outstanding_balance=loan.outstanding_balance,
                status=loan.status,
                created_at=loan.created_at.isoformat(),
                due_date=loan.due_date.isoformat()
            )
            for loan in loans
        ]