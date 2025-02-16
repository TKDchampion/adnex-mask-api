from sqlalchemy.orm import Session
from app.models.user import User
from app.models.pharmacy import Pharmacy
from app.models.mask import Mask
from app.models.purchase_history import PurchaseHistory

class PurchaseRepo:
    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_pharmacy(db: Session, pharmacy_id: int):
        return db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()

    @staticmethod
    def get_mask(db: Session, mask_id: int, pharmacy_id: int):
        return db.query(Mask).filter(Mask.id == mask_id, Mask.pharmacy_id == pharmacy_id).first()

    @staticmethod
    def update_user_balance(db: Session, user: User, prev_updated_at):
        return (
            db.query(User)
            .filter(User.id == user.id, User.updated_at == prev_updated_at)  # 確保 updated_at 沒變
            .update({"cash_balance": user.cash_balance, "updated_at": user.updated_at})
        )

    @staticmethod
    def update_pharmacy_balance(db: Session, pharmacy: Pharmacy, prev_updated_at):
        return (
            db.query(Pharmacy)
            .filter(Pharmacy.id == pharmacy.id, Pharmacy.updated_at == prev_updated_at)  # 確保 updated_at 沒變
            .update({"cash_balance": pharmacy.cash_balance, "updated_at": pharmacy.updated_at})
        )

    @staticmethod
    def create_purchase_history(db: Session, purchase_history: PurchaseHistory):
        db.add(purchase_history)