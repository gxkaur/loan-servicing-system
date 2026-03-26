import pandas as pd

def generate_summary_report(loans_df: pd.DataFrame) -> dict:
    total_loans = len(loans_df)
    total_outstanding = round(loans_df["outstanding_balance"].sum(), 2)

    paid_count = len(loans_df[loans_df["payment_status"] == "PAID"])
    partial_count = len(loans_df[loans_df["payment_status"] == "PARTIAL"])
    missed_count = len(loans_df[loans_df["payment_status"] == "MISSED"])

    total_carried_forward = round(loans_df["carried_forward_due"].sum(), 2)
    total_missed_payments = int(loans_df["missed_payment_count"].sum())

    return {
        "total_loans": total_loans,
        "total_outstanding_balance": total_outstanding,
        "paid_loans": paid_count,
        "partial_loans": partial_count,
        "missed_loans": missed_count,
        "total_carried_forward": total_carried_forward,
        "total_missed_payment_events": total_missed_payments
    }