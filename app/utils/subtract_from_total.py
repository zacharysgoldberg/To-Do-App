

# [subtract previous receipt amount from respective tax year total]


def subtract_from_total(_type, receipt_model, total_model, db):
    if _type == 'update':
        total_model.totals = float(
            total_model.totals) - float(receipt_model.total)
        total_model.tax_totals = float(
            total_model.tax_totals) - float(receipt_model.tax)

    else:
        total_model.totals = float(
            total_model.totals) - float(receipt_model.total)
        total_model.tax_totals = float(
            total_model.tax_totals) - float(receipt_model.tax)

    db.commit()
