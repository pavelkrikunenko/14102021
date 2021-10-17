from fastapi import FastAPI
from .database import engine, database
from . import models, database

app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
def shutdown():
    await database.disconnect()


from . import routes
