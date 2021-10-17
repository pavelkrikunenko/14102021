from sqlalchemy import create_engine, MetaData
import os
import databases

DATABASE_URL = os.environ.get('DATABASE_URL') or "sqlite:///./sql_app.db"
database = databases.Database(DATABASE_URL)

metadata = MetaData()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)


