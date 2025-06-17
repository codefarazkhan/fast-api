from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import get_current_user
from app.db.session import get_db_session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

router = APIRouter()

@router.post("/")
def create_todo(todo: TodoCreate, db=Depends(get_db_session), current_user=Depends(get_current_user)):
    db_todo = Todo(**todo.model_dump(), user_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/")
def read_todos(skip=0, limit=100, db=Depends(get_db_session), current_user=Depends(get_current_user)):
    todos = db.query(Todo).filter(Todo.user_id == current_user.id).offset(skip).limit(limit).all()
    return todos

@router.get("/{todo_id}")
def read_todo(todo_id, db=Depends(get_db_session), current_user=Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}")
def update_todo(todo_id, todo_update: TodoUpdate, db=Depends(get_db_session), current_user=Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    for key, value in todo_update.model_dump(exclude_unset=True).items():
        setattr(todo, key, value)
    
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id, db=Depends(get_db_session), current_user=Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return None 