from pydantic import BaseModel, EmailStr

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

    class Config:
        from_attributes = True  # This enables ORM mode

class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    email: str | None = None 