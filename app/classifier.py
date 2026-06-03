from sqlalchemy.orm import Session

from app.retrieval import get_vendor_rule


def classify_transaction(
    db: Session,
    vendor: str
):
    
    vendor_rule = get_vendor_rule(db, vendor)

    # Known vendor rule found
    if vendor_rule:
        return {
            "predicted_account": vendor_rule.account_name,
            "confidence_score": 0.98,
            "status": "AUTO_POSTED"
        }

    # Unknown vendor
    return {
        "predicted_account": None,
        "confidence_score": 0.30,
        "status": "PENDING_REVIEW"
    }