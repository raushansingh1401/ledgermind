from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    vendor = Column(String, nullable=False)
    description = Column(String, nullable=False)

    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)

    predicted_account = Column(String)
    confidence_score = Column(Float)

    status = Column(String)

    final_account = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


class VendorRule(Base):
    __tablename__ = "vendor_rules"

    id = Column(Integer, primary_key=True, index=True)

    vendor_name = Column(String, nullable=False)
    account_name = Column(String, nullable=False)

    usage_count = Column(Integer, default=1)

    confidence = Column(Float, default=1.0)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(Integer)

    predicted_account = Column(String)
    corrected_account = Column(String)

    reason = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)