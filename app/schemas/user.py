from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True  # This enables ORM mode

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    email: str | None = None 