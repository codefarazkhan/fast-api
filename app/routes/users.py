from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate
from app.db.dependencies import get_db
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
