from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from app.core.config import Settings

settings = Settings()

mongo_url = f"mongodb://{settings.MONGODB_USER}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"  # noqa: E501

mongo_engine = AsyncIOMotorClient(mongo_url)
db = mongo_engine[settings.MONGODB_DATABASE]
profiles_collection = db["profiles"]

sync_mongo_engine = MongoClient(mongo_url)
sync_db = sync_mongo_engine[settings.MONGODB_DATABASE]
sync_profiles_collection = sync_db["profiles"]
