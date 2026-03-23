from dataclasses import dataclass

@dataclass
class Loan:
    loan_id: str
    customer_id: str
    customer_name: str
    loan_amount: float
    annual_interest_rate: float
    term_months: int
    start_date: str
    monthly_due: float

    def monthly_interest_rate(self) -> float:
        return self.annual_interest_rate / 12 / 100

    def calculate_emi(self) -> float:
        r = self.monthly_interest_rate()
        n = self.term_months
        p = self.loan_amount

        if r == 0:
            return round(p / n, 2)

        emi = p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
        return round(emi, 2)