from sqlalchemy.orm import Session
from . import models, schemas
import random
import string
from datetime import datetime


async def get_users(db: Session, limit: int = 5, offset: int = 0):
    await db.query(models.User).limit(limit=limit).offset(offset).all()


async def get_user_count(db: Session):
    await db.query(models.User).all()


async def delete_user(id: int, db: Session):
    db_user = await db.query(models.User).filter(models.User.id == id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return False


async def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(
        name=user.name,
        role=user.role,
        ctime=int(datetime.timestamp(datetime.utcnow()))
    )
    await db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def generate_event():
    letters = string.ascii_letters
    rand_string = ''.join(random.choice(letters) for i in range(15))
    return rand_string
