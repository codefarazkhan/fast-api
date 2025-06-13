from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import get_current_user
from app.db.session import get_db_session
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate, Todo as TodoSchema

router = APIRouter()

@router.post("/", response_model=TodoSchema)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    db_todo = Todo(**todo.model_dump(), user_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/", response_model=List[TodoSchema])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    todos = db.query(Todo).filter(Todo.user_id == current_user.id).offset(skip).limit(limit).all()
    return todos

@router.get("/{todo_id}", response_model=TodoSchema)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoSchema)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return None 