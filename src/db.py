import psycopg2
import pandas as pd
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def fetch_loans():
    conn = get_connection()
    query = "SELECT * FROM loans;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def fetch_payments():
    conn = get_connection()
    query = "SELECT * FROM payments;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def fetch_payment_history():
    conn = get_connection()
    query = "SELECT * FROM payment_history ORDER BY history_id;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def update_loans(loans_df: pd.DataFrame):
    conn = get_connection()
    cur = conn.cursor()

    update_query = """
        UPDATE loans
        SET 
            outstanding_balance = %s,
            remaining_term_months = %s,
            next_due_date = %s,
            missed_payment_count = %s,
            carried_forward_due = %s
        WHERE loan_id = %s;
    """

    for _, row in loans_df.iterrows():
        cur.execute(
            update_query, 
            (
                float(row["outstanding_balance"]),
                int(row["remaining_term_months"]),
                row["next_due_date"],
                int(row["missed_payment_count"]),
                float(row["carried_forward_due"]),
                row["loan_id"],
            )
        )        

    conn.commit()
    cur.close()
    conn.close()


def insert_payment_history(payment_history_df: pd.DataFrame):
    conn = get_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO payment_history (
        loan_id,
        due_date,
        payment_date,
        scheduled_monthly_due,
        carried_forward_due_in,
        total_due,
        amount_paid,
        interest_due,
        interest_paid,
        principal_paid,
        unpaid_amount_carried_forward,
        remaining_balance,
        remaining_term_months,
        payment_status
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    for _, row in payment_history_df.iterrows():
        payment_date = row["payment_date"]
        if pd.isna(payment_date):
            payment_date = None

        cur.execute(
            insert_query,
            (
                row["loan_id"],
                row["due_date"],
                payment_date,
                float(row["scheduled_monthly_due"]),
                float(row["carried_forward_due_in"]),
                float(row["total_due"]),
                float(row["amount_paid"]),
                float(row["interest_due"]),
                float(row["interest_paid"]),
                float(row["principal_paid"]),
                float(row["unpaid_amount_carried_forward"]),
                float(row["remaining_balance"]),
                int(row["remaining_term_months"]),
                row["payment_status"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


def insert_payment(payment_id: str, loan_id: str, payment_date: str, amount_paid: float):
    conn = get_connection()
    cur = conn.cursor()

    insert_query = """
    INSERT INTO payments (payment_id, loan_id, payment_date, amount_paid)
    VALUES (%s, %s, %s, %s);
    """

    cur.execute(insert_query, (payment_id, loan_id, payment_date, amount_paid))
    conn.commit()

    cur.close()
    conn.close()