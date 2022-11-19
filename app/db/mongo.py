from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import Settings

settings = Settings()

mongo_url = f"mongodb://{settings.MONGODB_USER}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"  # noqa: E501

mongo_engine = AsyncIOMotorClient(mongo_url)
db = mongo_engine[settings.MONGODB_DATABASE]

profiles_collection = db["profiles"]
