from starlette import status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import engine, get_db
from pydantic import BaseModel
from models import Users, Base
from fastapi import APIRouter, Depends, Request, Form
from utils.security import get_current_user, hash_password, verify_password
import sys
sys.path.append("..")


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


# Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str
    

@router.get("/update-user", response_class=HTMLResponse)
async def update_password_view(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("update-user.html",
                                      {"request": request, "user": user})


@router.post('/update-user', response_class=HTMLResponse)
async def update_password(request: Request, username: str = Form(...),
                          password: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)

    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    user_data = db.query(Users).filter(Users.username == username).first()

    msg = "Invalid username or password"

    if user_data:
        if username == user_data.username and verify_password(password, user_data.password):
            hashed_password = hash_password(new_password)
            user_data.password = hashed_password

            db.add(user_data)
            db.commit()
            
            msg = "Password updated"

    return templates.TemplateResponse("update-user.html",
                                      {
                                          "request": request,
                                          "user": user,
                                          "msg": msg
                                      })


@router.get('/delete-account')
async def delete_account(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model:
        db.delete(user_model)
        db.commit()

        msg = "Account deleted succesfully"

        return templates.TemplateResponse("login.html",
                                          {"request": request, "msg": msg})
