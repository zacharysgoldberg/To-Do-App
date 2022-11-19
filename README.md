# Receipt Manager

## Description

Submit receipts to account to keep track of expendetures as well as total sales tax spent per fiscal/tax year.
Totals are calculated respectively.

## Design

FastAPI backend, bootstrap frontend, PostgreSQL, SQLAlchemy, Alembic, Nginx, Docker, and Kubernetes manifests.

## Features

- JavaScript FullCalendar CDN
- Integrated [Receipt-OCR](https://github.com/Asprise/receipt-ocr) API for scanning uploaded receipt files and retrieving/parsing relevant data from them.
- Reset password

## Future Improvements

- Receipt and Totals search/lookup tool.

## Hosted on AWS

[http://receipt-manager-env.us-west-1.elasticbeanstalk.com/](http://receipt-manager-env.us-west-1.elasticbeanstalk.com/)
