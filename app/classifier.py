from sqlalchemy.orm import Session

from app.retrieval import get_vendor_rule
from app.llm_classifier import classify_vendor


AUTO_POST_THRESHOLD = 0.90


def classify_transaction(
    db: Session,
    vendor: str,
    description: str
):

    # Step 1: Check learned vendor rules
    vendor_rule = get_vendor_rule(db, vendor)

    if vendor_rule:
        return {
            "predicted_account": vendor_rule.account_name,
            "confidence_score": vendor_rule.confidence,
            "status": "AUTO_POSTED"
        }

    # Step 2: Ask Gemini
    llm_result = classify_vendor(
        vendor=vendor,
        description=description
    )

    confidence = float(llm_result["confidence"])
    category = llm_result["category"]

    # Step 3: Confidence Routing

    if confidence >= AUTO_POST_THRESHOLD:
        return {
            "predicted_account": category,
            "confidence_score": confidence,
            "status": "AUTO_POSTED"
        }

    return {
        "predicted_account": category,
        "confidence_score": confidence,
        "status": "PENDING_REVIEW"
    }