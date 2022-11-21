from models import Receipt, Total
from .update_total import update_total
from .filter_items import filter_items
from utils.validate import validate_date_time


def existing_year(data, user_id, year, db):
    total_model = db.query(Total).filter(
        Total.tax_year == year).first()

    # [filter through json object to calculate purchase total]
    try:
        items = filter_items(data['items'])
        total = abs(data['subtotal'] + data['tax'])

    except:
        items = data['items_services']
        total = abs(data['total'])

    date, time = validate_date_time(data['date'], data['time'])

    # receipt_model = Receipt()
    # receipt_model.merchant_name = data['merchant_name']

    new_receipt = Receipt(
        merchant_name=data['merchant_name'],
        total=float(total),
        tax=float(data['tax']),
        merchant_address=data['merchant_address'],
        items_services=items,
        transaction_number=str(
            data['transaction_number']) if 'transaction_number' in data else None,
        card_last_4=data['credit_card_number'],
        link=data['merchant_website'],
        date=date,
        time=time,
        total_id=total_model.id,
        user_id=user_id
    )

    db.add(new_receipt)
    # [update existing total (tax year)]
    update_total('sum', total_model, data['date'][0:4],
                 total, data['tax'], user_id, db)

    db.commit()

    return new_receipt
