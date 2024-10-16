from fastapi import APIRouter, Depends, HTTPException, Path, Response, Request
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from starlette import status
from models import Todos
from pydantic import BaseModel, Field
from .auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]

class post_todos(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=10, max_length=100)
    priority : int = Field(gt=0, lt=6)
    complete : bool = Field(default= False)


@router.get("/")
def read_all_todos(user: user_dependency, db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get("/todos/{todo-id}", status_code=status.HTTP_200_OK)
def read_all_todos(db: Annotated[Session, Depends(get_db)], todos_id : int):
    todo_model = db.query(Todos).filter(Todos.id == todos_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Value Not Found')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user : user_dependency, db: Annotated[Session, Depends(get_db)], todo_request : post_todos):
    if user is None:
        raise HTTPException(status_code=401, detail= 'Authentication Failed')
    todos_model = Todos(**todo_request.model_dump(), owner_id = user.get('id'))

    db.add(todos_model)
    db.commit()

@router.put("/todo/{todo_id}")
async def update_todo(user : user_dependency, db: Annotated[Session, Depends(get_db)], todo_request : post_todos, todos_id : int):
    todo_model = db.query(Todos).filter(Todos.id == todos_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail= 'todo not dfound')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
    


@router.delete("/todos/{todo-id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: Annotated[Session, Depends(get_db)], todo_id : int):
        todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
        if todo_model is None:
            raise HTTPException(status_code=404, detail='Record Not Found')
        db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
        
        db.commit()

