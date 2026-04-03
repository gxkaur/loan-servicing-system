import os
import pandas as pd
from loan import Loan
from payment_processor import process_monthly_servicing
from reporting import generate_summary_report
from db_utils import fetch_loans, fetch_payments, update_loans, insert_payment_history

def add_monthly_due(loans_df: pd.DataFrame) -> pd.DataFrame:
    enriched_rows = []

    for _, row in loans_df.iterrows():
        loan = Loan(
            loan_id=row["loan_id"],
            customer_id=row["customer_id"],
            customer_name=row["customer_name"],
            loan_amount=float(row["loan_amount"]),
            annual_interest_rate=float(row["annual_interest_rate"]),
            term_months=int(row["term_months"]),
            start_date=row["start_date"],
        )

        row_dict = row.to_dict()
        row_dict["monthly_due"] = loan.calculate_emi()

        if "carried_forward_due" not in row_dict:
            row_dict["carried_forward_due"] = 0.0

        enriched_rows.append(row_dict)

    return pd.DataFrame(enriched_rows)


def main():
    output_dir = os.path.join("..", "data", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    loans_df = fetch_loans()
    payments_df = fetch_payments()

    loans_df = add_monthly_due(loans_df)

    updated_loans_df, payment_history_df = process_monthly_servicing(loans_df, payments_df)

    update_loans(updated_loans_df)
    insert_payment_history(payment_history_df)

    updated_loans_path = os.path.join(output_dir, "updated_loans.csv")
    payment_history_path = os.path.join(output_dir, "payment_history.csv")

    updated_loans_df.to_csv(updated_loans_path, index=False)
    payment_history_df.to_csv(payment_history_path, index=False)

    summary = generate_summary_report(updated_loans_df)

    print("Loan Servicing Summary")
    print("-" * 30)
    for key, value in summary.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()