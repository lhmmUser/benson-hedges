from typing import Optional
from ..db.mongo import get_collection
from ..domain.models.conversation import Conversation

_COLLECTION_NAME = "conversations"

class ConversationRepository:
    def __init__(self):
        self.collection = get_collection(_COLLECTION_NAME)

    def get_by_flow_id(self, flow_id: str) -> Optional[Conversation]:
        doc = self.collection.find_one({"flow_id": flow_id})
        if not doc:
            return None
        return Conversation(**doc)

    def get_active_by_user(self, user_id: str) -> Optional[Conversation]:
        doc = self.collection.find_one(
            {"user_id": user_id, "current_state": {"$nin": ["COMPLETED", "FAILED"]}}
        )
        if not doc:
            return None
        return Conversation(**doc)

    def create(self, conversation: Conversation) -> None:
        self.collection.insert_one(conversation.dict())

    def update(self, conversation: Conversation) -> None:
        conversation.touch()
        self.collection.update_one(
            {"flow_id": conversation.flow_id},
            {"$set": conversation.dict()},
            upsert=False,
        )
