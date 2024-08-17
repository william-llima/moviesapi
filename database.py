from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from bson import ObjectId

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.movie_recommendation_db

# Conexão síncrona para operações administrativas
admin_client = MongoClient("mongodb://localhost:27017")
admin_db = admin_client.movie_recommendation_db