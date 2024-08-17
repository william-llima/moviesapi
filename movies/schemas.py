from pydantic import BaseModel
from typing import List

class MovieResponse(BaseModel):
    title: str
    genre_ids: List[int]
    director: str
    actors: List[str]
    vote_average: float
    vote_count: int
    overview: str
    release_date: str

class Rating(BaseModel):
    movie_id: int
    rating: int