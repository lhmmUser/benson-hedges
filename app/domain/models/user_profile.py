from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    user_id: str = Field(...)
    whatsapp_number: str = Field(...)
    default_name: Optional[str] = None
    default_gender: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
