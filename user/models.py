from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    watched_movies: List[PyObjectId]
    ratings: List[dict]  # [{"movie_id": ObjectId, "rating": float}]
    favorite_genres: List[int]
    favorite_directors: List[str]
    favorite_actors: List[str]
    email: str | None
    full_name: str | None
    password:str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None
