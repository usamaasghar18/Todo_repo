from fastapi import APIRouter, Depends,HTTPException
from starlette import status
from typing import Annotated
from pydantic import BaseModel,Field
from database import SessionLocal
from sqlalchemy.orm import Session
import models
from models import users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from .auth import get_current_user


router = APIRouter(
    prefix='/users',
    tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password : str
    new_password : str = Field(min_length=5)

class EditNumber(BaseModel):
    phone_number : str
    new_phone_number : str

@router.get("/user")
async def get_user(user: user_dependency, db: Annotated[Session, Depends(get_db)]):
    user = db.query(users).filter(users.id == user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=401, detail= 'Authentication Failed')
    return user

@router.put("/Change_password")
async def Change_Password(user: user_dependency, db: Annotated[Session, Depends(get_db)], user_verification : UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail= 'Authentication Failed')
    user_model = db.query(users).filter(users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail= "Cant't Change")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put("/update-phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: Annotated[Session, Depends(get_db)], phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail= 'Authentication Failed')
    user_model = db.query(users).filter(users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()

@router.put("/Change-Number")
async def Change_Number(user: user_dependency, db: Annotated[Session, Depends(get_db)], edit_number : EditNumber):
    if user is None:
        raise HTTPException(status_code=401, detail= 'Authentication Failed')
    user_model = db.query(users).filter(users.id == user.get('id')).first()
    user_model.phone_number = edit_number.new_phone_number
    db.add(user_model)
    db.commit()
    