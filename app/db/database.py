import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables
load_dotenv()

# Database configuration
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "fastapi_db")

# Create database URL
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create database engine
try:
    engine = create_engine(
        DB_URL,
        echo=os.getenv("DB_ECHO", "false").lower() == "true"
    )
except SQLAlchemyError as e:
    raise Exception(f"Failed to create database engine: {str(e)}")

# Create declarative base
Base = declarative_base()
