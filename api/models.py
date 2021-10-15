from sqlalchemy import String, Column, Integer
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    role = Column(String(250), nullable=False)
    ctime = Column(Integer, default=int(datetime.timestamp(datetime.utcnow())))
