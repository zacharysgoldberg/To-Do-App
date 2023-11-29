# Receipt Manager

## Description

Submit receipts to account to keep track of expendetures as well as total sales tax spent per fiscal/tax year.
Totals are calculated respectively.

## Design

FastAPI backend, bootstrap frontend, PostgreSQL, SQLAlchemy, Alembic, Nginx reverse-proxy, unit, integration, and system tests. Streamlined CI/CD using GitHub Actions workflow. Automated build using Docker, tests with PyUnit (Unittest), and deployment with Kubernetes manifests.

## Features

- JavaScript FullCalendar CDN
- Integrated [Receipt-OCR](https://github.com/Asprise/receipt-ocr) API for scanning uploaded receipt files and retrieving/parsing relevant data from them.
- Reset password

## Future Improvements

- Receipt and Totals search/lookup tool.

## Live Link

* Link: [http://receipt-manager-env.us-west-1.elasticbeanstalk.com/](http://receipt-manager-env.us-west-1.elasticbeanstalk.com/)
