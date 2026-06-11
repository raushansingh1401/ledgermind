from sqlalchemy.orm import Session

from app.models import (
    Transaction,
    Feedback,
    VendorRule
)


def apply_feedback(
    db: Session,
    transaction_id: int,
    corrected_account: str,
    reason: str = None
):

    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        return None

    # Store audit trail
    feedback = Feedback(
        transaction_id=transaction.id,
        predicted_account=transaction.predicted_account,
        corrected_account=corrected_account,
        reason=reason
    )

    db.add(feedback)

    # Update transaction
    transaction.final_account = corrected_account
    transaction.status = "REVIEWED"

    # Learn vendor rule
    existing_rule = (
        db.query(VendorRule)
        .filter(
            VendorRule.vendor_name == transaction.vendor
        )
        .first()
    )

    if existing_rule:
        existing_rule.account_name = corrected_account
        existing_rule.usage_count += 1

    else:
        new_rule = VendorRule(
            vendor_name=transaction.vendor,
            account_name=corrected_account,
            usage_count=1,
            confidence=0.95
        )

        db.add(new_rule)

    db.commit()

    return transaction