from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from ...core.enums import ConversationState, ConsentStatus, BuddyApprovalStatus

class Conversation(BaseModel):
    flow_id: str = Field(...)
    user_id: str = Field(...)
    current_state: ConversationState = ConversationState.NEW_USER

    tnc_accepted: bool = False
    scene: Optional[str] = None

    user_name: Optional[str] = None
    user_gender: Optional[str] = None
    user_picture_url: Optional[str] = None

    buddy_name: Optional[str] = None
    buddy_gender: Optional[str] = None
    buddy_picture_url: Optional[str] = None

    consent_status: ConsentStatus = ConsentStatus.PENDING
    buddy_approval_status: BuddyApprovalStatus = BuddyApprovalStatus.PENDING

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()
