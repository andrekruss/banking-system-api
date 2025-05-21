from beanie import Document, PydanticObjectId
from datetime import datetime, timezone
from enum import Enum

from pydantic import Field

class PaymentType(str, Enum):
    PIX = "pix"
    BOLETO = "boleto"

class Payment(Document):
    user_id: PydanticObjectId
    account_id: PydanticObjectId
    payment_type: PaymentType
    target_identifier: str
    amount: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))