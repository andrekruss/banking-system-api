from enum import Enum
from beanie import Document, PydanticObjectId
from datetime import date, datetime, timezone
from pydantic import Field

class LoanStatus(str, Enum):
    ACTIVE = "active"
    PAID_OFF = "paid_off"
    DEFAULTED = "defaulted"

class Loan(Document):
    user_id: PydanticObjectId
    account_id: PydanticObjectId
    amount: float
    interest_rate: float
    installments: int
    installment_amount: float
    outstanding_balance: float
    status: LoanStatus = LoanStatus.ACTIVE
    due_date: date
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))