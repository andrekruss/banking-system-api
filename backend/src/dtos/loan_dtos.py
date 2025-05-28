from datetime import date
from pydantic import BaseModel

from src.database.models.loan import LoanStatus

class CreateLoanDTO(BaseModel):
    amount: float
    interest_rate: float
    installments: int
    due_date: date

class LoanDTO(BaseModel):
    id: str
    amount: float
    interest_rate: float
    installments: int
    installment_amount: float
    outstanding_balance: float
    status: LoanStatus
    created_at: str
    due_date: str