from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace these with your actual DB credentials
DB_URL = "mysql+pymysql://root:root@localhost:3306/fastapi_check"

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
