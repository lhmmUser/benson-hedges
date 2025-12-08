from typing import Optional
from ..db.mongo import get_collection
from ..domain.models.buddy_state import BuddyState

_COLLECTION_NAME = "buddy_states"

class BuddyStateRepository:
    def __init__(self):
        self.collection = get_collection(_COLLECTION_NAME)

    def get_by_flow_id(self, flow_id: str) -> Optional[BuddyState]:
        doc = self.collection.find_one({"flow_id": flow_id})
        if not doc:
            return None
        return BuddyState(**doc)

    def create(self, buddy_state: BuddyState) -> None:
        self.collection.insert_one(buddy_state.dict())

    def update(self, buddy_state: BuddyState) -> None:
        buddy_state.touch()
        self.collection.update_one(
            {"buddy_state_id": buddy_state.buddy_state_id},
            {"$set": buddy_state.dict()},
            upsert=False,
        )
