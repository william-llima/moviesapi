from pydantic import BaseModel
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
    
class UserCreate(BaseModel):
    email: str 
    full_name: str 
    password:str

class WatchedMovie(BaseModel):
    movieid:int
    
