from fastapi import FastAPI, HTTPException, Body, Request
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []
current_id = 0


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/')
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'user_list': users})


@app.get(path='/user/{user_id}')
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user", response_model=User)
async def create_user(user: User) -> RedirectResponse:
    global current_id
    current_id += 1
    new_user = User(id=current_id, username=user.username, age=user.age)
    users.append(new_user)
    return RedirectResponse(url=f"/user/{new_user.id}", status_code=302)


@app.put('/user/{user_id}', response_model=User)
async def update_user(user_id: int, username: str, age: int) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> User:
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")


