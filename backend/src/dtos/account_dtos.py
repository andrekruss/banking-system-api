from beanie import PydanticObjectId
from pydantic import BaseModel

class CreateAccountDTO(BaseModel):
    user_id: PydanticObjectId
    balance: float

class AccountDTO(BaseModel):
    id: str
    balance: float
    created_at: str