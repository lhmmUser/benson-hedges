from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from ...core.enums import BuddyApprovalStatus

class BuddyState(BaseModel):
    buddy_state_id: str = Field(...)
    flow_id: str = Field(...)

    buddy_name: Optional[str] = None
    buddy_gender: Optional[str] = None
    buddy_picture_url: Optional[str] = None

    approval_status: BuddyApprovalStatus = BuddyApprovalStatus.PENDING

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
