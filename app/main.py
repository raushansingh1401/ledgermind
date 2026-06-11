from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.classifier import classify_transaction
from app.database import engine, get_db
from app.models import Base, Transaction, VendorRule
from app.schemas import (
    TransactionCreate,
    TransactionResponse,
    FeedbackCreate
)
from app.feedback import apply_feedback

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Reap CFO Agent API is running"
    }


@app.post("/transactions", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):

    classification = classify_transaction(
        db=db,
        vendor=transaction.vendor
    )

    db_transaction = Transaction(
        vendor=transaction.vendor,
        description=transaction.description,
        amount=transaction.amount,
        currency=transaction.currency,

        predicted_account=classification["predicted_account"],
        confidence_score=classification["confidence_score"],
        status=classification["status"]
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction

@app.post("/feedback")
def submit_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):

    transaction = apply_feedback(
        db=db,
        transaction_id=feedback.transaction_id,
        corrected_account=feedback.corrected_account,
        reason=feedback.reason
    )

    if not transaction:
        return {
            "error": "Transaction not found"
        }

    return {
        "message": "Feedback applied successfully",
        "transaction_id": transaction.id,
        "final_account": transaction.final_account
    }

@app.get("/seed-rules")
def seed_rules(db: Session = Depends(get_db)):

    aws_rule = VendorRule(
        vendor_name="AWS",
        account_name="Cloud Infrastructure",
        usage_count=10,
        confidence=0.98
    )

    notion_rule = VendorRule(
        vendor_name="Notion Labs",
        account_name="SaaS Tools",
        usage_count=8,
        confidence=0.97
    )

    db.add(aws_rule)
    db.add(notion_rule)

    db.commit()

    return {
        "message": "Vendor rules inserted successfully"
    }