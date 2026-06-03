from sqlalchemy.orm import Session
from app.models import VendorRule


def get_vendor_rule(db: Session, vendor_name: str):
    
    return (
        db.query(VendorRule)
        .filter(VendorRule.vendor_name == vendor_name)
        .first()
    )