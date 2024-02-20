from fastapi import Request, Depends, Form, APIRouter
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models import User, Base
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
async def register_user(request: Request,
                        username: str = Form(...),
                        email: str = Form(...),
                        email2: str = Form(...),
                        password: str = Form(...),
                        confirm_password: str = Form(...),
                        db: Session = Depends(get_db)):
    validate_username = db.query(User).filter(
        User.username == username).first()
    validate_email = db.query(User).filter(User.email == email).first()

    if validate_username is not None or validate_email is not None:
        msg = "Email or Username is already in use"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})
    if email != email2:
        msg = "Emails do not match"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})
    if password != confirm_password:
        msg = 'Passwords not not match'
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

    user_model = User()
    user_model.email = email
    user_model.username = username

    hashed_password = hash_password(password)
    user_model.password = hashed_password

    db.add(user_model)
    db.commit()

    msg = "User successfully created"
    return templates.TemplateResponse('login.html', {"request": request, "msg": msg})
