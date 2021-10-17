from sqlalchemy import String, Column, Integer, Table
from .database import metadata
from datetime import datetime


users = Table(
    'users',
    metadata,
    Column('id', Integer,
           primary_key=True,
           index=True),
    Column('name',String(250),
           unique=True, nullable=False),
    Column('role',String(250), nullable=False),
    Column('ctime', Integer,
           default=int(datetime.timestamp(datetime.utcnow())))
)
