from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

from loan import Loan
from payment_processor import process_monthly_servicing
from reporting import generate_summary_report
from servicing_utils import add_monthly_due
from db_utils import (
    fetch_loans, 
    fetch_payments,
    fetch_payment_history, 
    insert_payment,
    update_loans,
    insert_payment_history
)

app = FastAPI(title="Loan Servicing API")

class PaymentCreate(BaseModel):
    payment_id: str
    loan_id: str
    payment_date: str
    amount_paid: float


# ----------------
# GET Endpoints
# ----------------
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Loan Servicing API is running"}


@app.get("/loans")
def get_loans():
    loans_df = fetch_loans()
    return loans_df.to_dict(orient="records")


@app.get("/loans/{loan_id}")
def get_loan_by_id(loan_id: str):
    loans_df = fetch_loans()
    loan_df = loans_df[loans_df["loan_id"] == loan_id]

    if loan_df.empty:
        raise HTTPException(status_code=404, detail=f"Loan {loan_id} not found")

    return loan_df.to_dict(orient="records")[0]


@app.get("/payment-history")
def get_payment_history():
    history_df = fetch_payment_history()
    return history_df.to_dict(orient="records")


# -----------------
# POST Endpoints
# -----------------
@app.post("/payments")
def create_payment(payment: PaymentCreate):
    loans_df = fetch_loans()
    loan_df = loans_df[loans_df["loan_id"] == payment.loan_id]

    if loan_df.empty:
        raise HTTPException(status_code=404, detail=f"Loan {payment.loan_id} not found")

    try:
        insert_payment(
            payment_id=payment.payment_id,
            loan_id=payment.loan_id,
            payment_date=payment.payment_date,
            amount_paid=payment.amount_paid,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "message": "Payment inserted successfully",
        "payment_id": payment.payment_id,
        "loan_id": payment.loan_id,
    }


@app.post("/servicing/run")
def run_servicing_cycle():
    try:
        loans_df = fetch_loans()
        payments_df = fetch_payments()

        loans_df = add_monthly_due(loans_df)

        updated_loans_df, payment_history_df = process_monthly_servicing(loans_df, payments_df)

        update_loans(updated_loans_df)
        insert_payment_history(payment_history_df)

        summary = generate_summary_report(updated_loans_df)

        return {
            "message": "Monthly servicing cycle completed successfully",
            "summary": summary,
            "processed_loans": len(updated_loans_df),
            "history_records_inserted": len(payment_history_df),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))