from fastapi import FastAPI
from .database import engine, get_db
from . import models, database


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.state.database = get_db

from . import routes
