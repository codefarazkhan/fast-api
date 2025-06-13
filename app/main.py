from fastapi import FastAPI
from app.routes import users
from app.db.database import Base, engine
from app.models import user  # ✅ Import models before create_all

app = FastAPI()

# Create tables in DB
Base.metadata.create_all(bind=engine)

app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI + MySQL"}
