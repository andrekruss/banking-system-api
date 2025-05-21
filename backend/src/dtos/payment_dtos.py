from pydantic import BaseModel

from src.database.models.payment import PaymentType

class CreatePaymentDTO(BaseModel):
    # user_id: str
    # account_id: str
    payment_type: PaymentType
    target_identifier: str
    amount: float

class PaymentDTO(BaseModel):
    account_id: str
    payment_type: PaymentType
    target_identifier: str
    amount: float
    created_at: str