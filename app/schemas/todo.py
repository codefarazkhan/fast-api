from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    title: Optional[str] = None

class TodoInDBBase(TodoBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Todo(TodoInDBBase):
    pass 