from sqlalchemy import Column, Integer, String, Boolean # type: ignore
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    profile_image = Column(String(255), nullable=True)
    
    todos = relationship("Todo", back_populates="user")
