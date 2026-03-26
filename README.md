# Loan Servicing & Payment Processing System

## Overview

This project simulates a real-world **loan servicing system** that processes borrower payments, tracks outstanding balances, and manages loan lifecycle states such as full, partial, and missed payments.

It is designed to reflect how financial institutions handle **monthly loan servicing cycles**, including interest calculation, principal allocation, delinquency tracking, and carry-forward of unpaid dues.

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
- Structured output reports for loan status and payment history

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
│ ├── main.py
│ ├── loan.py
│ ├── payment_processor.py
│ ├── reporting.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Tech Stack

- **Python**
- **Pandas**
- **Dataclasses**
- **Git & GitHub**

---

## How It Works

1. Loan data is ingested from CSV
2. EMI is calculated dynamically based on loan parameters
3. A monthly servicing cycle is executed:
   - Interest is calculated on outstanding balance
   - Payment is applied
   - Split into interest and principal
4. System determines payment status:
   - `PAID`
   - `PARTIAL`
   - `MISSED`
5. Unpaid amounts are carried forward
6. Loan state is updated:
   - Remaining balance
   - Remaining term
   - Next due date
   - Missed payment count
7. Reports are generated

---

## How to Run

### 1. Install dependencies
`pip install -r requirements.txt`
### 2. Run the application
```
cd src
python main.py
```
---

## Sample Output

The system generates:

- `updated_loans.csv` → latest loan state
- `payment_history.csv` → detailed servicing records

---

## What This Project Demonstrates

- Backend system design for financial workflows
- Data processing and transformation pipelines
- Implementation of real-world business logic
- State management across time-based cycles
- Handling of edge cases (partial/missed payments)

---

## Future Enhancements

- Database integration (SQLite/PostgreSQL)
- AWS integration (S3, Lambda, API Gateway)
- Dashboard using Streamlit
- Late fee and penalty calculations
- Multi-cycle simulation engine
- REST API layer using FastAPI

---

## Disclaimer

This project is a simplified simulation of a loan servicing system built for learning and demonstration purposes. It does not represent any proprietary or production system.

---

## Author

Built as part of a hands-on portfolio to demonstrate backend, data processing, and cloud-ready system design.