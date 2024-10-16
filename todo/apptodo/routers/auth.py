from fastapi import APIRouter, Depends,HTTPException
from starlette import status
from typing import Annotated
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
import models
from models import users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    email : str
    first_name: str
    last_name: str
    password: str
    role:str
    phone_number : str

class Token(BaseModel):
    access_token: str
    token_type: str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username : str, password : str, db):
    user = db.query(users).filter(users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username : str, user_id : int, role : str, expires_delta : timedelta):
    encode = {'sub' : username, 'id' : user_id, 'role' : role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role : str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= 'user not valid')
        return {'username' : username, 'id': user_id, 'user_role' : user_role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= 'user not valid')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request : CreateUserRequest):

    create_user_model = users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role.lower(),
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True,
        phone_number = create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= 'user not valid')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}

