from fastapi import Request, Depends, Form, APIRouter
from models import User, Base
from database import get_db
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .auth import templates
from utils.send_email import send_email
from utils.security import hash_password, create_access_token
from datetime import timedelta
from fastapi import BackgroundTasks
import os

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {"description": "Not found"}}
)


@router.get('/forgot-password', response_class=HTMLResponse)
async def forgot_password_view(request: Request):
    return templates.TemplateResponse("forgot-password.html", {'request': request})


@router.post('/forgot-password', response_class=HTMLResponse)
async def forgot_password(request: Request,
                          background_tasks: BackgroundTasks,
                          email: str = Form(...),
                          db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        # Make token expire after 1 hour
        # reset_token = str(uuid.uuid1())
        reset_token = create_access_token(
            user.username,
            user.id,
            expires_delta=timedelta(minutes=60)
        )

        subject = "Hello"
        recipient = [email]
        msg = f"Hello, {user.username}\n\nA request has been made to reset your password.\nIf this was not you, please ignore this message.\nOtherwise, go ahead and follow the link below.\nhttp://{os.getenv('EXTERNAL_IP')}/auth/reset-password/?reset_token={reset_token}\nYour password will not change until you access the link above and create a new one."

        send_email(subject, recipient, msg, background_tasks)

        user.reset_token = reset_token
        db.add(user)
        db.commit()

    msg = f"A link will be sent to {email} if an account exists for it"
    return templates.TemplateResponse('forgot-password.html', {'request': request, 'msg': msg})


@router.get('/reset-password/', response_class=HTMLResponse)
async def reset_password_view(request: Request, reset_token: str):
    return templates.TemplateResponse("reset-password.html", {'request': request, 'reset_token': reset_token})


@router.post('/reset-password/', response_class=HTMLResponse)
async def reset_password(request: Request, reset_token: str, new_password: str = Form(...),
                         confirm_password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.reset_token == reset_token).first()

    if user:
        if new_password == confirm_password:
            user.password = hash_password(new_password)
            user.reset_token = None

            db.add(user)
            db.commit()

            msg = "Password sucessfully updated"
            return templates.TemplateResponse('reset-password.html', {'request': request, 'msg': msg})

        msg = "Passwords do not match"
        return templates.TemplateResponse('reset-password.html', {'request': request, 'email': reset_token, 'msg': msg})

    msg = "Invalid Token"
    return templates.TemplateResponse('reset-password.html', {'request': request, 'msg': msg})
