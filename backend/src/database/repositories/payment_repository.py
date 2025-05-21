from beanie import PydanticObjectId
from datetime import datetime, timezone

from src.database.models.payment import Payment
from src.dtos.payment_dtos import CreatePaymentDTO, PaymentDTO

class PaymentRepository:

    async def create(self, user_id: PydanticObjectId, account_id: PydanticObjectId, create_payment_dto: CreatePaymentDTO) -> PaymentDTO:

        payment = Payment(
            user_id=user_id,
            account_id=account_id,
            payment_type=create_payment_dto.payment_type,
            target_identifier=create_payment_dto.target_identifier,
            amount=create_payment_dto.amount,
            created_at=datetime.now(timezone.utc)
        )

        await payment.insert()

        return PaymentDTO(
            account_id=str(account_id),
            payment_type=payment.payment_type,
            target_identifier=payment.target_identifier,
            amount=payment.amount,
            created_at=str(payment.created_at)
        )

        