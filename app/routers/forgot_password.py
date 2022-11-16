from fastapi import Request, Depends, Form, APIRouter
from models import Users, Base
from database import get_db
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .auth import templates
from utils.send_email import send_email
from utils.security import hash_password, create_access_token
from datetime import timedelta
import uuid
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
async def forgot_password(request: Request, email: str = Form(...),
                          db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == email).first()
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
        message = """
        <!DOCTYPE html>
        <html>
        <title>Reset Password</title>
        <body>
        <div style="width:100%;font-family: monospace;">
            <h2>Hello, {0:}</h2>
            <p>Someone has requested a link to reset your password. If you requested this, you can change your password through the link provided below.</p>
            <a href="http://{1:}/auth/reset-password/?reset_token={2:}" style="box-sizing:border-box;border-color:#1f8feb;border:solid 1px #1f8feb;border-radius:4px;color:#ffffff;font-size:16px;font-weight:bold;margin:0;padding:12px text-transform:capitalize">Reset Your Password</a>
            <p>If you did not request this, you can ignore this email.</p>
            <p>Your password will not change until you access the link above and create a new one.</p>
        </div>
        </body>
        </html>
        """.format(email, os.getenv('EXTERNAL_IP'), reset_token)

        await send_email(subject, recipient, message)

        user.reset_token = reset_token
        db.add(user)
        db.commit()

    msg = f"A link has been sent to {email}"
    return templates.TemplateResponse('forgot-password.html', {'request': request, 'msg': msg})


@router.get('/reset-password/', response_class=HTMLResponse)
async def reset_password_view(request: Request, reset_token: str):
    return templates.TemplateResponse("reset-password.html", {'request': request, 'reset_token': reset_token})


@router.post('/reset-password/{reset_token}', response_class=HTMLResponse)
async def reset_password(request: Request, reset_token: str, new_password: str = Form(...),
                         confirm_password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Users).filter(
        Users.reset_token == reset_token).first()

    print("===================")
    print(reset_token)
    print("===================")

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
