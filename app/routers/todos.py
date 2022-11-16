from fastapi import Depends, HTTPException, APIRouter, Request, Form
from starlette.responses import RedirectResponse
from starlette import status
from models import ToDos, Base
from database import engine, get_db
from sqlalchemy.orm import Session
from utils.security import get_current_user
from datetime import datetime
from . import templates

from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

# Base.metadata.create_all(bind=engine)

# [Rendering todos as a list to dashboard]


@router.get('/', response_class=HTMLResponse)
async def get_all_by_user(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    todos = db.query(ToDos).filter(ToDos.user_id == user.get('id')).all()

    return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user})

# [Rendering todos onto calendar]


@router.get('/calendar', response_class=HTMLResponse)
async def calendar(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    events = db.query(ToDos).filter(ToDos.user_id == user.get('id')).all()

    return templates.TemplateResponse("calendar.html", {'request': request, 'user': user, "events": events})

# [Rendering todo page]


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...),
                      description: str = Form(...),
                      priority: int = Form(...),
                      date: str = Form(...),
                      db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    todo_model = ToDos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.date = date
    todo_model.complete = False

    todo_model.user_id = user.get('id')

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

# [Rendering edit todo page]


@router.get('/edit-todo/{todo_id}', response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    todo = db.query(ToDos).filter(ToDos.id == todo_id).first()

    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})


@router.post('/edit-todo/{todo_id}', response_class=HTMLResponse)
async def edit_todo_commit(request: Request, todo_id: int,
                           title: str = Form(...),
                           description: str = Form(...),
                           priority: int = Form(...),
                           date: str = Form(...),
                           db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()

    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.date = date

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get('/delete/{todo_id}')
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).filter(
        ToDos.user_id == user.get('id')).first()

    if todo_model is None:
        return RedirectResponse(url="/toDos", status_code=status.HTTP_302_FOUND)

    db.query(ToDos).filter(ToDos.id == todo_id).delete()
    db.commit()

    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)

# {Completing a todo and rendering results on dashboard}


@router.get('/complete/{todo_id}', response_class=HTMLResponse)
async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    todo = db.query(ToDos).filter(ToDos.id == todo_id).first()

    # [changing it to the opposite (True)]
    todo.complete = not todo.complete

    db.add(todo)
    db.commit()

    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)
