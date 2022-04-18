import email
from pyexpat import model
from fastapi import FastAPI, Depends
from h11 import InformationalResponse
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    password: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Base.metadata.create_all(engine)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


@app.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.hash_password = get_password_hash(create_user.password)

    db.add(create_user_model)
    db.commit()

    return create_user_model
