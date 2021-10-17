from . import app, schemas, crud, request
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, WebSocket
from datetime import datetime
from .database import SessionLocal
import asyncio


@app.on_event('startup')
async def startup():
    app.state.database()


@app.on_event('shutdown')
def shutdown():
    SessionLocal.close_all()


@app.post('/user/', response_model=schemas.User)
async def create_user(user: schemas.UserBase, db: Session = Depends(app.state.database)):
    await crud.create_user(db=db, user=user)


@app.get('/api/users/list')
async def get_users(limit: int = 5, offset: int = 0, db: Session = Depends(app.state.database)):
    db_users = await crud.get_users(db=db, limit=limit, offset=offset)
    all_users = await crud.get_user_count(db=db)
    return {
        'total': len(all_users),
        'per_page': limit,
        'page': 1,
        'limit': limit,
        'offset': offset,
        'items': db_users
    }


@app.delete('/api/user/{id}', status_code=204)
async def delete_user(id: int, db: Session = Depends(app.state.database)):
    db_user = await crud.delete_user(id=id, db=db)
    if db_user:
        return HTTPException(status_code=status.HTTP_200_OK,
                             detail='User deleted')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='User not found')


@app.websocket('/event')
async def event(websocket: WebSocket):
    await websocket.accept()
    i = 0

    while True:
        if i != 0:
            await asyncio.sleep(10)
        event_string = await crud.generate_event()
        i += 1
        await websocket.send_json({'ctime': int(datetime.timestamp(datetime.utcnow())),
                                   'event': event_string})
