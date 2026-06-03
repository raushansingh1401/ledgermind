from pydantic import BaseModel
from typing import Optional


class TransactionCreate(BaseModel):
    vendor: str
    description: str
    amount: float
    currency: str


class TransactionResponse(BaseModel):
    id: int
    vendor: str
    description: str
    amount: float
    currency: str

    predicted_account: Optional[str]
    confidence_score: Optional[float]

    status: Optional[str]

    class Config:
        from_attributes = True