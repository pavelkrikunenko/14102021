from fastapi import FastAPI
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

from . import routes
