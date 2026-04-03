from pydantic import BaseModel


class PaymentCreate(BaseModel):
    payment_id: str
    loan_id: str
    payment_date: str
    amount_paid: float