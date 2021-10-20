from fastapi import FastAPI
from .database import engine, database
from . import models, database

app = FastAPI()
app.state.db = database


@app.on_event('startup')
async def startup():
    await app.state.db.connect()


@app.on_event('shutdown')
async def shutdown():
    await app.state.db.disconnect()


from . import routes
