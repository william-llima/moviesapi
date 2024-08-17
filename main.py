from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from bson import ObjectId
from typing import List
from movies.models import *
from user.models import *
from movies.schemas import *
from user.schemas import *
from user.view import *
from database import db
import json

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],  # Permita todos os métodos (ou especifique POST, GET, etc.)
    allow_headers=["*"],  # Permita todos os headers (ou especifique)
)

def json_serializer(data):
    if isinstance(data, ObjectId):
        return str(data)
    raise TypeError("Type not serializable")

"""
User Route
"""

@app.post("/token", )
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):    
    return await login_for_access_token_view(form_data)

@app.post("/users/create",)
async def create_user(user_data: UserCreate):
    return await create_user_view(user_data)

"""
End User Route
"""

"""
Movie Route
"""

@app.get("/filmes",)
async def get_all_movies(current_user: User = Depends(get_current_user)):
    if not 'movies' in await db.list_collection_names():
        with open('./db.json','r',encoding='utf-8') as file:
            file_data = json.load(file)
            if 'results' in file_data:
                db.movies.insert_many(file_data['results'])
           
    movies = await db.movies.find().to_list(100)
    return json.loads(json.dumps(movies, default=json_serializer))

@app.post("/usuarios/avaliacoes")
async def add_rating(rating:Rating,current_user: User = Depends(get_current_user)):
   
    await db.movies.update_one(
        {"id": rating.movie_id},
        {"$set":{'rating':rating.rating}}
    )

    return "Avaliação adicionada com sucesso"

@app.post("/usuarios/watchedmovies")
async def add_rating(wm: WatchedMovie,current_user: User = Depends(get_current_user)):
    
    if current_user and wm.movieid not in current_user.get('watched_movies', []):
        await db.users.update_one(
            {"_id": ObjectId(current_user['_id'])},
            {"$push": {"watched_movies": wm.movieid}}
        )
        await db.movies.update_one(
            {"id": wm.movieid},
            {"$set": { "watched": True }}
        )
    return "filme adicionado na lista"

@app.get("/filmes/{usuario_id}/recomendacoes")
async def get_recommendations(usuario_id: str,current_user: User = Depends(get_current_user)):
    user = await db.users.find_one({"_id": ObjectId(usuario_id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    await db.movies.update_many(
        {"rating": {"$exists": False}},  # Filtro para documentos sem o campo 'rating'
        {"$set": {"rating": 0}}  # Define o valor padrão para 'rating'
    )
    await db.movies.update_many(
        {"watched": {"$exists": False}},  # Filtro para documentos sem o campo 'rating'
        {"$set": {"watched": False}}  # Define o valor padrão para 'rating'
    )
    primeira_busca = await db.movies.find({"watched": True}).sort("rating", -1).to_list(100)
    listmovies=[]
    idsMoviesSelected=[]
    if not primeira_busca:
        movies = await db.movies.find().to_list(100)
        return json.loads(json.dumps(movies, default=json_serializer))
    else:
        for i in primeira_busca:
           if(i['id'] not in idsMoviesSelected):
                    idsMoviesSelected.append(i['id']) 
        for i in primeira_busca:
            genremovies = await db.movies.find({"genre_ids":i["genre_ids"],"id": {"$nin": idsMoviesSelected}}).to_list(None)
            listmovies +=genremovies
            for j in listmovies:
                if(j['id'] not in idsMoviesSelected):
                    idsMoviesSelected.append(i['id'])
            
            genremovies =  await db.movies.find({"genre_ids": {"$in": i["genre_ids"]},"id": {"$nin": idsMoviesSelected}}).to_list(None)
            print(len(genremovies))
            listmovies +=genremovies
            for i in listmovies:
                if(i['id'] not in idsMoviesSelected):
                    idsMoviesSelected.append(i['id'])
        genremovies = await db.movies.find({"id":{"$nin":idsMoviesSelected}}).to_list(None)  
        
        listmovies +=genremovies  
    return json.loads(json.dumps(listmovies, default=json_serializer))
