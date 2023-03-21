#config.py
from fastapi import FastAPI
from pydantic import BaseSettings
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#env_path = Path('.') / '.env'
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME","VTUAPI")
    PROJECT_VERSION: str = "1.0.1"
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT : str = os.getenv(" POSTGRES_PORT","5432") # default postgres port is 5432
    POSTGRES_DB : str = os.getenv("POSTGRES_DB")
   # DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    DATABASE_URL = os.getenv("DATABASE_URLSQL")
    SECRET_KEY :str = os.getenv("SECRET_KEY")   
    ALGORITHM = "HS256"                         
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  
    TEST_USER_EMAIL = "test@example.com"


settings = Settings()
