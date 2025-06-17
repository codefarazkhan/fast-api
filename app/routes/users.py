from fastapi import APIRouter, Depends, HTTPException, status, Body, UploadFile, File, Form 
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserSignIn, UserProfileUpdate
from app.db.session import get_db_session
from app.core.auth import create_access_token, verify_password, get_password_hash, get_current_user
from datetime import timedelta
import os
import shutil
from typing import Optional

router = APIRouter()

@router.get("/users")
def get_users(db=Depends(get_db_session)):
    users = db.query(UserModel).all()
    return users

@router.post("/users")
def create_user(user: UserCreate, db=Depends(get_db_session)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token}

@router.post("/signin")
# def signin(user_data: UserSignIn = Body(...), db=Depends(get_db_session)):
def signin(user_data: UserSignIn, db=Depends(get_db_session)):
    db_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token}

@router.put("/users/profile")
async def update_profile(
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    current_user: UserModel = Depends(get_current_user),
    db=Depends(get_db_session)
):
    # Update profile data if provided
    if name:
        current_user.name = name
    if email:
        # Check if email is already taken
        existing_user = db.query(UserModel).filter(
            UserModel.email == email,
            UserModel.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = email

    # Handle profile image upload
    if profile_image:
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads/profile_images"
        os.makedirs(upload_dir, exist_ok=True)

        # Generate unique filename
        file_extension = os.path.splitext(profile_image.filename)[1]
        filename = f"profile_{current_user.id}{file_extension}"
        file_path = os.path.join(upload_dir, filename)

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_image.file, buffer)

        # Update user's profile image path
        current_user.profile_image = f"/uploads/profile_images/{filename}"

    db.commit()
    db.refresh(current_user)
    return current_user
