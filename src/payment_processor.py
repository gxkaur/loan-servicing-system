import pandas as pd

def process_payments(loans_df: pd.DataFrame, payments_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    updated_loans = []
    payment_history = []

    for _, loan in loans_df.iterrows():
        loan_id = loan["loan_id"]
        payment_row = payments_df[payments_df["loan_id"] == loan_id]

        amount_paid = 0.0
        payment_date = None

        if not payment_row.empty:
            amount_paid = float(payment_row.iloc[0]["amount_paid"])
            payment_date = payment_row.iloc[0]["payment_date"]

        outstanding_balance = float(loan.get("outstanding_balance", loan["loan_amount"]))
        annual_rate = float(loan["annual_interest_rate"])
        monthly_rate = annual_rate / 12 / 100
        interest_due = round(outstanding_balance * monthly_rate, 2)
        principal_paid = round(max(amount_paid - interest_due, 0), 2)

        if principal_paid > outstanding_balance:
            principal_paid = outstanding_balance

        new_balance = round(outstanding_balance - principal_paid, 2)

        if amount_paid == 0:
            payment_status = "MISSED"
        elif amount_paid < float(loan["monthly_due"]):
            payment_status = "PARTIAL"
        else:
            payment_status = "PAID"

        updated_loan = loan.to_dict()
        updated_loan["outstanding_balance"] = new_balance
        updated_loan["last_payment_date"] = payment_date
        updated_loan["last_payment_amount"] = amount_paid
        updated_loan["payment_status"] = payment_status

        updated_loans.append(updated_loan)

        payment_history.append({
            "loan_id": loan_id,
            "payment_date": payment_date,
            "amount_paid": amount_paid,
            "interest_due": interest_due,
            "principal_paid": principal_paid,
            "remaining_balance": new_balance,
            "payment_status": payment_status
        })

    return pd.DataFrame(updated_loans), pd.DataFrame(payment_history)