
from . import schemas
import random
import string
from datetime import datetime

from .models import users


async def get_users(db):
    query = users.select()
    return await db.fetch_all(query)


async def get_user_count(db):
    return await db.fetch_all(users.select())


async def delete_user(id: int, db):
    query = f"""DELETE FROM users WHERE id={id}"""
    return await db.execute(query)


async def create_user(user: schemas.UserBase, db):
    ctime = int(datetime.timestamp(datetime.utcnow()))
    query = users.insert()
    values = {'name': user.name,
              'role': user.role,
              'ctime': ctime}
    return await db.execute(query, values=values)


async def generate_event():
    letters = string.ascii_letters
    rand_string = ''.join(random.choice(letters) for i in range(15))
    return rand_string
