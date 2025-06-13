from fastapi import FastAPI
from app.routes import users, todo
from app.db.session import Base, engine

app = FastAPI()

# Create tables in DB
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(todo.router, prefix="/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "FastAPI + MySQL"}
