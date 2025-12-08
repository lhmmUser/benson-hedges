from pymongo import MongoClient
from typing import Any
from ..config import get_settings

_client = None
_db = None

def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        settings = get_settings()
        _client = MongoClient(str(settings.MONGO_URI))
    return _client

def get_database():
    global _db
    if _db is None:
        settings = get_settings()
        _db = get_mongo_client()[settings.MONGO_DB_NAME]
    return _db

def get_collection(name: str):
    db = get_database()
    return db[name]
