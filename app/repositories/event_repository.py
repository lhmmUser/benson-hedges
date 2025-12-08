from typing import List
from ..db.mongo import get_collection
from ..domain.models.event_log import EventLog

_COLLECTION_NAME = "events"

class EventRepository:
    def __init__(self):
        self.collection = get_collection(_COLLECTION_NAME)

    def create(self, event: EventLog) -> None:
        self.collection.insert_one(event.dict())

    def list_by_flow_id(self, flow_id: str) -> List[EventLog]:
        docs = self.collection.find({"flow_id": flow_id}).sort("created_at", 1)
        return [EventLog(**doc) for doc in docs]
