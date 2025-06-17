from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import users, todo
from app.db.database import engine
from app.models import user, todo as todo_model
import os

# Create database tables
user.Base.metadata.create_all(bind=engine)
todo_model.Base.metadata.create_all(bind=engine)

# Create uploads directory if it doesn't exist
os.makedirs("uploads/profile_images", exist_ok=True)

app = FastAPI()

# Mount static files directory for profile images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(users.router, tags=["users"])
app.include_router(todo.router, prefix="/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "FastAPI + MySQL"}
