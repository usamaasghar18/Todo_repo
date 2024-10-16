from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from starlette import status
from models import Todos, users
from pydantic import BaseModel, Field
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/todo')
async def read_all(user : user_dependency, db: Annotated[Session, Depends(get_db)]):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail= 'Authentication Failed')
    return db.query(Todos).all()

@router.get("/users")
async def get_all_user(user: user_dependency, db: Annotated[Session, Depends(get_db)]):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail= 'Authentication Failed')
    return db.query(users).all()