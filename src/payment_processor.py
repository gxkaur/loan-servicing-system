import pandas as pd

LATE_FEE_AMOUNT = 25.00     # Flat late fee applied when a payment is missed or partially paid
PENALTY_RATE = 0.02         # 2% of the unpaid amount as a penalty for late payment


def add_one_month(date_str: str) -> str:
    date = pd.to_datetime(date_str)
    next_date = date + pd.DateOffset(months=1)
    return next_date.strftime("%Y-%m-%d")


def assess_delinquency_charges(amount_paid: float, total_due: float, unpaid_amount: float) -> tuple[float, float]:
    late_fee_applied = 0.0
    penalty_applied = 0.0

    if amount_paid < total_due:
        late_fee_applied = LATE_FEE_AMOUNT
        penalty_applied = round(unpaid_amount * PENALTY_RATE, 2)

    return late_fee_applied, penalty_applied


def process_monthly_servicing(loans_df: pd.DataFrame, payments_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
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

        outstanding_balance = float(loan["outstanding_balance"])
        annual_rate = float(loan["annual_interest_rate"])
        monthly_due = float(loan["monthly_due"])
        remaining_term_months = int(loan["remaining_term_months"])
        missed_payment_count = int(loan["missed_payment_count"])
        due_date = loan["next_due_date"]
        carried_forward_due = float(loan.get("carried_forward_due", 0.0))
        late_fee_due = float(loan.get("late_fee_due", 0.0))
        penalty_due = float(loan.get("penalty_due", 0.0))

        monthly_rate = annual_rate / 12 / 100        
        interest_due = round(outstanding_balance * monthly_rate, 2)

        total_due = round(monthly_due + carried_forward_due + late_fee_due + penalty_due, 2)

        interest_paid = round(min(amount_paid, interest_due), 2)
        principal_paid = round(max(amount_paid - interest_paid, 0), 2)

        if principal_paid > outstanding_balance:
            principal_paid = outstanding_balance

        new_balance = round(outstanding_balance - principal_paid, 2)

        unpaid_amount = round(max(total_due - amount_paid, 0), 2)

        if amount_paid == 0:
            payment_status = "MISSED"
            missed_payment_count += 1
        elif amount_paid < total_due:
            payment_status = "PARTIAL"
            missed_payment_count += 1
        else:
            payment_status = "PAID"

        late_fee_applied, penalty_applied = assess_delinquency_charges(
            amount_paid=amount_paid,
            total_due=total_due,
            unpaid_amount=unpaid_amount,
        )

        if amount_paid >= monthly_due and remaining_term_months > 0:
            remaining_term_months -= 1

        updated_loan = loan.to_dict()
        updated_loan["outstanding_balance"] = new_balance
        updated_loan["remaining_term_months"] = remaining_term_months
        updated_loan["next_due_date"] = add_one_month(due_date)
        updated_loan["missed_payment_count"] = missed_payment_count
        updated_loan["last_payment_date"] = payment_date
        updated_loan["last_payment_amount"] = amount_paid
        updated_loan["payment_status"] = payment_status
        updated_loan["carried_forward_due"] = unpaid_amount
        updated_loan["late_fee_due"] = round(late_fee_due + late_fee_applied, 2)
        updated_loan["penalty_due"] = round(penalty_due + penalty_applied, 2)

        updated_loans.append(updated_loan)

        payment_history.append({
            "loan_id": loan_id,
            "due_date": due_date,
            "payment_date": payment_date,
            "scheduled_monthly_due": monthly_due,
            "carried_forward_due_in": carried_forward_due,
            "total_due": total_due,
            "amount_paid": amount_paid,
            "interest_due": interest_due,
            "interest_paid": interest_paid,
            "principal_paid": principal_paid,
            "unpaid_amount_carried_forward": unpaid_amount,
            "remaining_balance": new_balance,
            "remaining_term_months": remaining_term_months,
            "payment_status": payment_status,
            "late_fee_applied": late_fee_applied,
            "penalty_applied": penalty_applied
        })

    return pd.DataFrame(updated_loans), pd.DataFrame(payment_history)