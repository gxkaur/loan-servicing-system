import os
import pandas as pd
from payment_processor import process_payments
from reporting import generate_summary_report

def main():
    loans_path = os.path.join("data", "loans.csv")
    payments_path = os.path.join("data", "payments.csv")
    output_dir = os.path.join("data", "outputs")

    os.makedirs(output_dir, exist_ok=True)

    loans_df = pd.read_csv(loans_path)
    payments_df = pd.read_csv(payments_path)

    loans_df["outstanding_balance"] = loans_df["loan_amount"]

    updated_loans_df, payment_history_df = process_payments(loans_df, payments_df)

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