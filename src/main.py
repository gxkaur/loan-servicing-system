import os
from db import (
    fetch_loans, 
    fetch_payments, 
    update_loans, 
    insert_payment_history
)
from servicing_service import run_servicing_cycle
from reporting import generate_summary_report


def main():
    output_dir = os.path.join("..", "data", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    loans_df = fetch_loans()
    payments_df = fetch_payments()

    updated_loans_df, payment_history_df = run_servicing_cycle(loans_df, payments_df)

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