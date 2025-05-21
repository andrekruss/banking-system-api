from beanie import Document, PydanticObjectId
from datetime import datetime, timezone
from pydantic import Field

class Account(Document):
    user_id: PydanticObjectId
    balance: float = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))