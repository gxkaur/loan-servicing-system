import pandas as pd
from loan import Loan


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
            start_date=str(row["start_date"]),
        )

        row_dict = row.to_dict()
        row_dict["monthly_due"] = loan.calculate_emi()

        if "carried_forward_due" not in row_dict or pd.isna(row_dict["carried_forward_due"]):
            row_dict["carried_forward_due"] = 0.0

        enriched_rows.append(row_dict)

    return pd.DataFrame(enriched_rows)