
from . import schemas
import random
import string
from datetime import datetime
from .database import database
from .models import users


async def get_users(limit: int = 5, offset: int = 0):
    query = users.select().limit(limit).offset(offset)
    return await database.fetch_all(query)


async def get_user_count():
    return await database.fetch_all(users.select())


async def delete_user(id: int):
    query = f"""DELETE FROM users WHERE id={id}"""
    return await database.execute(query)


async def create_user(user: schemas.UserBase):
    ctime = int(datetime.timestamp(datetime.utcnow()))
    query = users.insert()
    values = {'name': user.name,
              'role': user.role,
              'ctime': ctime}
    return await database.execute(query, values=values)


async def generate_event():
    letters = string.ascii_letters
    rand_string = ''.join(random.choice(letters) for i in range(15))
    return rand_string
