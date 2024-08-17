
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException,status
from .models import *
from .schemas import *
from datetime import datetime, timedelta
from database import db
from config import *



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserInDB(User):
    hashed_password: str
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(email: str):
   
   existing_user = await db.users.find_one({"email": email})
   
   return existing_user


async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_user_view(user_data: UserCreate):
    try:
        existing_user = await db.users.find_one({"email": user_data.email})
        
        if existing_user:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
        user = User(
            watched_movies=[],
            ratings=[],
            favorite_genres=[],
            favorite_directors=[],
            favorite_actors=[],
            email=user_data.email,
            full_name=user_data.full_name,
            password=get_password_hash(user_data.password),
        )
        result = await db.users.insert_one(user.model_dump(by_alias=True))
        return str('Succes user created')
    except Exception as e:
        print(e)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                         detail="Error in user creation",)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError as e:
        
        raise credential_exception

    user = await get_user(token_data.username)
    
    if user is None:
        raise credential_exception

    return user

async def login_for_access_token_view(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email'],"id":str(ObjectId(user['_id']))}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

