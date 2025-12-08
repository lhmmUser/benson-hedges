from typing import Optional
from ..db.mongo import get_collection
from ..domain.models.user_profile import UserProfile

_COLLECTION_NAME = "users"

class UserRepository:
    def __init__(self):
        self.collection = get_collection(_COLLECTION_NAME)

    def get_by_whatsapp_number(self, number: str) -> Optional[UserProfile]:
        doc = self.collection.find_one({"whatsapp_number": number})
        if not doc:
            return None
        return UserProfile(**doc)

    def get_by_user_id(self, user_id: str) -> Optional[UserProfile]:
        doc = self.collection.find_one({"user_id": user_id})
        if not doc:
            return None
        return UserProfile(**doc)

    def create(self, user: UserProfile) -> None:
        self.collection.insert_one(user.dict())

    def update(self, user: UserProfile) -> None:
        user.touch()
        self.collection.update_one(
            {"user_id": user.user_id},
            {"$set": user.dict()},
            upsert=False,
        )
