from typing import Optional
from ..db.mongo import get_collection
from ..domain.models.consent import ConsentRecord

_COLLECTION_NAME = "consents"

class ConsentRepository:
    def __init__(self):
        self.collection = get_collection(_COLLECTION_NAME)

    def get_by_flow_id(self, flow_id: str) -> Optional[ConsentRecord]:
        doc = self.collection.find_one({"flow_id": flow_id})
        if not doc:
            return None
        return ConsentRecord(**doc)

    def create(self, consent: ConsentRecord) -> None:
        self.collection.insert_one(consent.dict())

    def update(self, consent: ConsentRecord) -> None:
        consent.touch()
        self.collection.update_one(
            {"consent_id": consent.consent_id},
            {"$set": consent.dict()},
            upsert=False,
        )
