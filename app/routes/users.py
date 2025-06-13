from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate, UserSignIn, Token
from app.db.session import get_db
from app.core.auth import create_access_token, verify_password, get_password_hash
from typing import List
from datetime import timedelta

router = APIRouter()

@router.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.post("/users", response_model=Token)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user with email already exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create access token
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token}

@router.post("/signin", response_model=Token)
def signin(user_data: UserSignIn, db: Session = Depends(get_db)):
    # Find user by email
    db_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token}
