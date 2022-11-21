from fastapi import Depends, HTTPException, APIRouter, Request, Form, UploadFile
from starlette.responses import RedirectResponse
from starlette import status
from models import Receipt, Base, User, Total
from database import engine, get_db
from sqlalchemy.orm import Session
from utils.security import get_current_user
from utils import existing_year, new_year, subtract_from_total, update_total
from utils.receipt_ocr import receipt_ocr
from . import templates
from fastapi.responses import HTMLResponse
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable, Optional
from datetime import datetime
# from .reminder import reminder
# from fastapi import BackgroundTasks

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
# Receipt file upload helper functions

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


# [Add receipt with uploaded file]


@router.post("/add-receipt", response_class=HTMLResponse)
async def add_receipt(request: Request,
                      file: UploadFile,
                      db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    # [Uploaded receipt file and save to a temporary path for universal accessibility]
    tmp_path = save_upload_file_tmp(file)
    # print(tmp_path)
    try:
        receipt = receipt_ocr(tmp_path)
    finally:
        # [remove receipt file from temporary path]
        tmp_path.unlink()

    user_id = user.get('id')

    """email = db.query(Users.email).filter(
        Users.username == user['username']).first()
    reminder(date, email[0], title, background_tasks)"""

    try:
        # [add new receipt to existing tax year total]
        existing_year.existing_year(
            receipt[0], user_id, receipt[0]['date'][0:4], db)
    except BaseException:
        # [add new receipt to new tax year total]
        new_year.new_year(receipt[0], user_id, db)

    return RedirectResponse(url="/receipts", status_code=status.HTTP_302_FOUND)


# [Manually add receipt]


@router.post('/add-receipt-manually', response_class=HTMLResponse)
async def add_receipt_manually(request: Request,
                               merchant_name: str = Form(...),
                               total: float = Form(...),
                               tax: float = Form(...),
                               merchant_address: str = Form(...),
                               items_services: str = Form(...),
                               transaction_number: Optional[str] = Form(None),
                               card_last_4: Optional[str] = Form(None),
                               merchant_website: Optional[str] = Form(None),
                               date: str = Form(...),
                               time: Optional[str] = Form(None),
                               db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    receipt = [{'merchant_name': merchant_name, 'total': total,
                'tax': tax, 'merchant_address': merchant_address,
                'items_services': items_services,
                'transaction_number': transaction_number if transaction_number else None,
                'credit_card_number': card_last_4, 'merchant_website': merchant_website,
                'date': date, 'time': time}]

    user_id = user.get('id')
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


# TODO: [Update a receipt]

@ router.get('/update-receipt/{receipt_id}', response_class=HTMLResponse)
async def update_receipt_view(request: Request, receipt_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()

    return templates.TemplateResponse("update-receipt.html", {"request": request, "receipt": receipt, "user": user})


@ router.post('/update-receipt/{receipt_id}', response_class=HTMLResponse)
async def update_receipt(request: Request, receipt_id: int,
                         merchant_name: str = Form(...),
                         merchant_address: str = Form(...),
                         total: float = Form(...),
                         tax: float = Form(...),
                         date: str = Form(...),
                         time: str = Form(None),
                         items_services: str = Form(...),
                         card_last_4: str = Form(None),
                         trasnaction_number: str = Form(None),
                         link: str = Form(None),
                         db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)

    receipt_model = db.query(Receipt).filter(Receipt.id == receipt_id).first()
    total_model = db.query(Total).filter(
        Total.tax_year == str(receipt_model.date)[0:4]).first()
    user_id = user.get('id')

    subtract_from_total.subtract_from_total(
        'update', receipt_model, total_model, db)

    receipt_model.merchant_name = merchant_name
    receipt_model.merchant_address = merchant_address
    receipt_model.total = total
    receipt_model.tax = tax
    receipt_model.date = date
    receipt_model.time = datetime.strptime(time, '%H:%M') if time else None
    receipt_model.items_services = items_services
    receipt_model.card_last_4 = card_last_4
    receipt_model.trasnaction_number = trasnaction_number
    receipt_model.link = link

    db.add(receipt_model)

    update_total.update_total('update', total_model,
                              date[0:4], total, tax, user_id, db)

    db.commit()

    return RedirectResponse(url="/receipts", status_code=status.HTTP_302_FOUND)


# [Delete receipt and update totals]

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

    total_model = db.query(Total).filter(Total.tax_year == tax_year).first()
    subtract_from_total.subtract_from_total('', receipt_model, total_model, db)

    db.query(Receipt).filter(Receipt.id == receipt_id).delete()
    db.commit()

    return RedirectResponse(url='/receipts', status_code=status.HTTP_302_FOUND)
