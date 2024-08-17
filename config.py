from pydantic_settings import BaseSettings, SettingsConfigDict 
class Config(BaseSettings):
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    model_config = SettingsConfigDict(env_file="../.env")
    
config=Config()
SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES