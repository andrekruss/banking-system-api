from beanie import PydanticObjectId
from datetime import datetime, timezone

from src.database.models.account import Account
from src.dtos.account_dtos import AccountDTO, CreateAccountDTO
from src.exceptions.account_exceptions import AccountNotFoundError

class AccountRepository:

    async def create(self, create_account_dto: CreateAccountDTO) -> AccountDTO:

        account = Account(
            user_id=create_account_dto.user_id,
            balance=create_account_dto.balance,
            created_at=datetime.now(timezone.utc)
        )
        await account.insert()

        return AccountDTO(
            id=str(account.id),
            balance=account.balance,
            created_at=str(account.created_at)
        )
    
    async def get_by_user_id(self, user_id: PydanticObjectId) -> AccountDTO:

        account = await Account.find_one(Account.user_id == user_id)

        if not account:
            raise AccountNotFoundError()
        
        return AccountDTO(
            id=str(account.id),
            balance=account.balance,
            created_at=str(account.created_at)
        )
    
        
        
        
