from . import app, schemas, crud
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, WebSocket
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
import asyncio

templates = Jinja2Templates(directory='api/templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/user/', response_model=schemas.User)
async def create_user(user: schemas.UserBase, db: Session = Depends(crud.get_db)):
    return crud.create_user(db=db, user=user)


@app.get('/api/users/list')
async def get_users(limit: int = 5, offset: int = 0, db: Session = Depends(crud.get_db)):
    db_users = crud.get_users(db=db, limit=limit, offset=offset)
    return {
        'total': crud.get_user_count(db=db),
        'per_page': limit,
        'page': 1,
        'limit': limit,
        'offset': offset,
        'items': db_users
    }


@app.delete('/api/user/{id}', status_code=204)
async def delete_user(id: int, db: Session = Depends(crud.get_db)):
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
