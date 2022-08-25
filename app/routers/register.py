from fastapi import Request, Depends, Form, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models import Users, Base
from database import get_db
from utils.security import hash_password
from .auth import templates

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {"description": "Not found"}}
)

@router.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post('/register', response_class=HTMLResponse)
async def register_user(request: Request, email: str = Form(...), username: str = Form(...),
                        firstname: str = Form(...), lastname: str = Form(...),
                        password: str = Form(...), password2: str = Form(...),
                        db: Session = Depends(get_db)):
    validate_username = db.query(Users).filter(
        Users.username == username).first()
    validate_email = db.query(Users).filter(Users.email == email).first()

    if password != password2 or validate_username is not None or validate_email is not None:
        msg = "Invalid registration request"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

    user_model = Users()
    user_model.email = email
    user_model.username = username
    user_model.first_name = firstname
    user_model.last_name = lastname

    hashed_password = hash_password(password)
    user_model.password = hashed_password

    db.add(user_model)
    db.commit()

    msg = "User successfully created"
    return templates.TemplateResponse('login.html', {"request": request, "msg": msg})