from sqlalchemy.orm import Session
from . import models, schemas
import random
import string
from fastapi import Depends
from .database import SessionLocal
from datetime import datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_users(db: Session = Depends(get_db), limit: int = 5, offset: int = 0):
    return db.query(models.User).limit(limit=limit).offset(offset).all()


def get_user_count(db: Session = Depends(get_db)):
    return len(db.query(models.User).all())


def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return False


def create_user(db: Depends(get_db), user: schemas.UserBase):
    db_user = models.User(
        name=user.name,
        role=user.role,
        ctime=int(datetime.timestamp(datetime.utcnow()))
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def generate_event():
    letters = string.ascii_letters
    rand_string = ''.join(random.choice(letters) for i in range(15))
    return rand_string
