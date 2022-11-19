from fastapi import Depends, HTTPException, APIRouter, Request
from starlette.responses import RedirectResponse
from starlette import status
from models import Total
from database import engine, get_db
from sqlalchemy.orm import Session
from utils.security import get_current_user
from . import templates
from fastapi.responses import HTMLResponse
import sys
# sys.path.append("..")


router = APIRouter(
    prefix="/totals",
    tags=["totals"],
    responses={404: {"description": "Not found"}}
)

# [get all totals for user]


@router.get('/', response_class=HTMLResponse)
async def get_all_user_totals(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    totals = db.query(Total).filter(
        Total.user_id == user.get('id')).order_by(Total.tax_year).all()
    print(totals)

    return templates.TemplateResponse("totals.html", {"request": request, "totals": totals, "user": user})
