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

class Movie(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    genre_ids: List[int]
    director: str
    actors: List[str]
    vote_average: float
    vote_count: int
    overview: str
    release_date: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Rating(BaseModel):
    movie_id: str
    rating: int