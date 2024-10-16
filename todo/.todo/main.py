from fastapi import FastAPI, APIRouter
import models
from models import Todos
from database import engine
from routers import todos, auth, admin, user


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)