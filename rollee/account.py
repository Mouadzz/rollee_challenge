from pydantic import BaseModel


class Account(BaseModel):
    account_id: str
    name: str
    email: str
    platform_name: str
    country: str
    currency: str
    gross_earnings: float
