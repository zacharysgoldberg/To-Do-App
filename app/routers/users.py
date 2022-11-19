from starlette import status
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import engine, get_db
from models import User, Base
from typing import Optional
from . import templates
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


@router.get("/update-user", response_class=HTMLResponse)
async def update_user_view(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("update-user.html",
                                      {"request": request, "user": user})


@router.post('/update-user', response_class=HTMLResponse)
async def update_user(request: Request,
                      email: Optional[str] = Form(None),
                      new_email: Optional[str] = Form(None),
                      password: Optional[str] = Form(None),
                      new_password: Optional[str] = Form(None),
                      db: Session = Depends(get_db)):
    user = await get_current_user(request)

    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    msg = "Account updated"
    user_id = user.get('id')
    user_data = db.query(User).filter(User.id == user_id).first()

    if email and new_email:
        user_exists = db.query(User).filter(
            User.email == new_email).first()
        if user_exists is None:
            user_data.email = new_email
            db.add(user_data)
            db.commit()

        else:
            msg = 'Email is already in use'
            return templates.TemplateResponse("update-user.html",
                                              {
                                                  "request": request,
                                                  "user": user,
                                                  "msg": msg
                                              })

    if password and verify_password(password, user_data.password) and new_password:
        hashed_password = hash_password(new_password)
        user_data.password = hashed_password

        db.add(user_data)
        db.commit()

    elif not password and email or password and not email:
        msg = 'No changes made'
        return templates.TemplateResponse("update-user.html",
                                          {
                                              "request": request,
                                              "user": user,
                                              "msg": msg
                                          })

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

    user_model = db.query(User).filter(User.id == user.get('id')).first()
    if user_model:
        db.delete(user_model)
        db.commit()

        msg = "Account deleted succesfully"

        return templates.TemplateResponse("login.html",
                                          {"request": request, "msg": msg})
