# Loan Servicing & Payment Processing System

## Overview

This project simulates a real-world **loan servicing system** that processes borrower payments, tracks outstanding balances, and manages loan lifecycle states such as full, partial, and missed payments. It is designed to reflect how financial institutions handle **monthly loan servicing cycles**, including interest calculation, principal allocation, delinquency tracking, and carry-forward of unpaid dues.

---

## Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **psycopg2**
- **Pandas**
- **Git & GitHub**

---

## Key Features

- Loan data ingestion from structured input
- EMI (Equated Monthly Installment) calculation using financial formulas
- Monthly servicing cycle processing
- Payment allocation into **interest and principal**
- Detection of:
  - Full payments
  - Partial payments
  - Missed payments
- Carry-forward of unpaid dues across cycles
- Automatic advancement of next due date
- Tracking of:
  - Outstanding balance
  - Remaining loan term
  - Missed payment count
- Persistent payment history tracking

---

## System Design (High Level)

Input Data → Processing Engine → Database → API / Reports

- **Processing Engine** handles loan servicing logic  
- **Database** maintains persistent loan and payment state  
- **API** enables interaction with the system  
- **Batch Runner** allows scheduled execution  

---

## Project Structure

```
loan-servicing-system/
│
├── data/
│ ├── loans.csv
│ ├── payments.csv
│ └── outputs/
│
├── src/
│ ├── app.py
│ ├── main.py
│ ├── config.py
│ ├── db.py
│ ├── schemas.py
│ ├── loan.py
│ ├── payment_processor.py
│ ├── servicing_service.py
│ ├── reporting.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to Run

### 1. Install dependencies
`pip install -r requirements.txt`
### 2. Set up environment variables
Create a `.env` file:
```
DB_NAME=loan_servicing
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```
### 3. Run API
```
cd src
uvicorn app:app --reload
```
Open
```
http://127.0.0.1:8000/docs
```

### 4. Run Batch Processing
```
cd src
python main.py
```
---
## Output

- Updates loan state in PostgreSQL
- Inserts records into `payment_history` DB table
- Generate CSV reports in `data/outputs/`

---

## What This Project Demonstrates

- Backend system design for financial workflows
- Data processing and transformation pipelines
- Implementation of real-world business logic for loan servicing
- State management across time-based cycles
- Handling of edge cases (partial/missed payments)
- API-driven service design
- Database integration with PostgreSQL

---

## Future Enhancements

- AWS integration (S3, Lambda, API Gateway)
- Dashboard using Streamlit
- Late fee and penalty calculations
- Multi-cycle simulation engine

---

## Disclaimer

This project is a simplified simulation of a loan servicing system built for learning and demonstration purposes. It does not represent any proprietary or production system.

---

## Author

Built as part of a hands-on portfolio to demonstrate backend, data processing, and cloud-ready system design.