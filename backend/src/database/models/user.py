from beanie import Document
from datetime import datetime, timezone
from pydantic import ConfigDict, EmailStr, Field

class User(Document):
    name: str = Field(max_length=100)
    cpf: str = Field(max_length=11, json_schema_extra={"unique": True})
    telephone: str = Field(max_length=15, json_schema_extra={"unique": True})
    email: EmailStr = Field(json_schema_extra={"unique": True})
    password: str = Field(max_length=256)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(arbitrary_types_allowed=True)
