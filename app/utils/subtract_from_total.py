

# [subtract previous receipt amount from respective tax year total]


def subtract_from_total(_type, receipt, total, db):
    if _type == 'purchase':
        total.purchase_totals = float(
            total.purchase_totals) - float(receipt.purchase_total)

    elif _type == 'tax':
        total.tax_totals = float(total.tax_totals) - float(receipt.tax)

    else:
        total.purchase_totals = float(
            total.purchase_totals) - float(receipt.purchase_total)
        total.tax_totals = float(total.tax_totals) - float(receipt.tax)

    db.commit()
