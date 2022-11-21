from models import Total, Receipt
from utils.validate import validate_date_time
from .filter_items import filter_items


def new_year(data, user_id, db):
    # [get row count]
    rows = db.query(Total).count()

    # [filter through json object to calculate purchase total]
    try:
        items = filter_items(data['items'])
        total = abs(data['subtotal'] + data['tax'])

    except:
        items = {'items': data['items_services']}
        total = abs(data['total'])

    # total_model = Total()
    # total_model.total = float(total)

    total_model = Total(
        totals=float(total),
        tax_totals=round(float(data['tax']), 2),
        tax_year=data['date'][0:4],
        user_id=user_id
    )
    db.add(total_model)

    date, time = validate_date_time(data['date'], data['time'])

    # receipt_model = Receipt()
    # receipt_mode._from = data['merchant_name']

    # [add new receipt for new tax year]
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
        total_id=rows + 1,
        user_id=user_id
    )

    db.add(new_receipt)
    db.commit()

    return new_receipt
