from fastapi import Depends, HTTPException, APIRouter, Request, Form, UploadFile
from starlette.responses import RedirectResponse
from starlette import status
from models import Receipt, Base, User, Total
from database import engine, get_db
from sqlalchemy.orm import Session
from utils.security import get_current_user
from utils import existing_year, new_year, subtract_from_total
from utils.receipt_ocr import receipt_ocr
from . import templates
from .reminder import reminder
from fastapi import BackgroundTasks
from fastapi.responses import HTMLResponse
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable

router = APIRouter(
    prefix="/receipts",
    tags=["receipts"],
    responses={404: {"description": "Not found"}}
)

# Base.metadata.create_all(bind=engine)

# [Rendering receipts as a list to dashboard]


@router.get('/', response_class=HTMLResponse)
async def get_all_user_receipts(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    receipts = db.query(Receipt).filter(
        Receipt.user_id == user.get('id')).order_by(Receipt.date).all()
    print(receipts)

    return templates.TemplateResponse("home.html", {"request": request, "receipts": receipts, "user": user})

# [Rendering receipts onto calendar]


@router.get('/calendar', response_class=HTMLResponse)
async def calendar(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    events = db.query(Receipt).filter(Receipt.user_id == user.get('id')).all()

    return templates.TemplateResponse("calendar.html", {'request': request, 'user': user, "events": events})

# [Rendering receipts page]


@router.get("/add-receipt", response_class=HTMLResponse)
async def add_new_receipt(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-receipt.html", {"request": request, "user": user})


# ==========================================================================================


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(upload_file: UploadFile, handler: Callable[[Path], None]) -> None:
    tmp_path = save_upload_file_tmp(upload_file)
    try:
        handler(tmp_path)  # Do something with the saved temp file
    finally:
        tmp_path.unlink()  # Delete the temp file


@router.post("/add-receipt", response_class=HTMLResponse)
async def add_receipt(request: Request,
                      file: UploadFile,
                      db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    tmp_path = save_upload_file_tmp(file)
    # print(tmp_path)
    try:
        receipt = receipt_ocr(tmp_path)
    finally:
        tmp_path.unlink()

    user_id = user.get('id')

    # email = db.query(Users.email).filter(
    #     Users.username == user['username']).first()
    # reminder(date, email[0], title, background_tasks)

    try:
        # [add new receipt to existing tax year total]
        existing_year.existing_year(
            receipt[0], user_id, receipt[0]['date'][0:4], db)
    except BaseException:
        # [add new receipt to new tax year total]
        new_year.new_year(receipt[0], user_id, db)

    return RedirectResponse(url="/receipts", status_code=status.HTTP_302_FOUND)


# [Rendering receipt details page]


@ router.get('/receipt-details/{receipt_id}', response_class=HTMLResponse)
async def receipt_details(request: Request, receipt_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()

    return templates.TemplateResponse("receipt-details.html", {"request": request, "receipt": receipt, "user": user})


"""@ router.post('/receipt-detais/{receipt_id}', response_class=HTMLResponse)
async def edit_receipt_details(request: Request, receipt_id: int,
                               title: str = Form(...),
                               description: str = Form(...),
                               priority: int = Form(...),
                               date: str = Form(...),
                               db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    todo_model = db.query(Receipt).filter(Receipt.id == receipt_id).first()

    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.date = date

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)"""


@ router.get('/delete/{receipt_id}')
async def delete_receipt(request: Request, receipt_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    receipt_model = db.query(Receipt).filter(Receipt.id == receipt_id).filter(
        Receipt.user_id == user.get('id')).first()

    if receipt_model is None:
        return RedirectResponse(url="/receipts", status_code=status.HTTP_302_FOUND)

    tax_year = str(receipt_model.date)[0:4]
    # total_id = db.query(Total.id).filter(
    #     Total.tax_year == tax_year).first()[0]
    total_model = db.query(Total).filter(Total.tax_year == tax_year).first()
    subtract_from_total.subtract_from_total('', receipt_model, total_model)

    db.query(Receipt).filter(Receipt.id == receipt_id).delete()
    db.commit()

    return RedirectResponse(url='/receipts', status_code=status.HTTP_302_FOUND)
