from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from ...core.enums import ConsentStatus

class ConsentRecord(BaseModel):
    consent_id: str = Field(...)
    flow_id: str = Field(...)
    user_id: str = Field(...)
    status: ConsentStatus = ConsentStatus.PENDING
    consent_type: str = "default"
    metadata: Dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
