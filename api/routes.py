from . import app, schemas, crud

from fastapi import status, HTTPException, WebSocket
from datetime import datetime
from sqlite3 import IntegrityError
import asyncio
from fastapi.requests import Request

@app.post('/user/')
async def create_user(user: schemas.UserBase, request: Request ):
    try:
        db_user = await crud.create_user(user=user, db=app.state.db)
        if db_user:
            return HTTPException(status_code=status.HTTP_201_CREATED,
                                 detail=f'User was created by {request.client.host}')
    except IntegrityError as e:
        return HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                             detail='This name already registered')


@app.get('/api/users/list')
async def get_users(limit: int = 5, offset: int = 0):
    db_users = await crud.get_users(limit=limit, offset=offset, db=app.state.db)
    all_users = await crud.get_user_count(db=app.state.db)
    return {
        'total': len(all_users),
        'per_page': limit,
        'page': 1,
        'limit': limit,
        'offset': offset,
        'items': db_users,

    }


@app.delete('/api/user/{id}')
async def delete_user(id: int):
    db_user = await crud.delete_user(id=id, db=app.state.db)

    if db_user:
        return HTTPException(status_code=status.HTTP_200_OK,
                             detail='User deleted')
    else:
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
