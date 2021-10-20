from . import app, schemas, crud
from fastapi import status, HTTPException, WebSocket
from datetime import datetime
from sqlite3 import IntegrityError
import asyncio
from fastapi.requests import Request
from .models import users


@app.post('/user/')
async def create_user(user: schemas.UserBase, request: Request):
    try:
        db_user = await crud.create_user(user=user, db=request.app.state.db)
        if db_user:
            return HTTPException(status_code=status.HTTP_201_CREATED,
                                 detail=f'User was created by {request.app.active_connection}')
    except IntegrityError as e:
        return HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                             detail='This name already registered')


@app.get('/api/users/list')
async def get_users(request: Request, limit: int = 5, offset: int = 0):
    query_with_limit = users.select().limit(limit).offset(offset)
    db_users = await request.app.state.db.fetch_all(query=query_with_limit)
    total = len(await crud.get_users(request.app.state.db))
    page = int((offset / limit) + 1)
    return {
        'total': total,
        'per_page': limit,
        'page': page,
        'limit': limit,
        'offset': offset,
        'items': db_users
    }


@app.delete('/api/user/{id}')
async def delete_user(id: int, request: Request):
    db_user = await crud.delete_user(id=id, db=request.app.state.db)

    if db_user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail='User deleted')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User not found')


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
