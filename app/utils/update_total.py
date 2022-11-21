from models import Total


# [update totals for respective tax year if user supplied tax year input exists]
def update_total(action, total_model, year, total, tax, user_id, db):
    if total_model.tax_year == year and action == 'sum':
        total_model.totals = round(float(total_model.totals) + float(total), 2)
        total_model.tax_totals = round(
            float(total_model.tax_totals) + float(tax), 2)

    elif total_model.tax_year == year and action == 'update':
        total_model.totals = round(float(total_model.totals) + float(total), 2)
        total_model.tax_totals = round(
            float(total_model.tax_totals) + float(tax), 2)

    else:
        # [create new tax year total]
        total = Total(
            totals=round(total, 2),
            tax_totals=round(tax, 2),
            tax_year=year,
            user_id=user_id
        )
        db.add(total)
