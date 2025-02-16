from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import HTTPException

from app.repositories.purchase_repo import PurchaseRepo
from app.models.purchase_history import PurchaseHistory


class PurchaseService:
    @staticmethod
    def process_purchase(db: Session, user_id: int, pharmacy_id: int, mask_id: int, quantity: int):
        """
        Buy Mask Deals based on ACID rules
        1. 檢查 user, pharmacy, mask 是否存在
        2. Check user's balance
        3. Use ACID：
            - minus `users.cash_balance`
            - add `pharmacies.cash_balance`
            - transaction
        4. Use Optimistic Locking `updated_at`, Preventing race conditions
        """

        user = PurchaseRepo.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_prev_updated_at = user.updated_at

        pharmacy = PurchaseRepo.get_pharmacy(db, pharmacy_id)
        if not pharmacy:
            raise HTTPException(status_code=404, detail="Pharmacy not found")
        pharmacy_prev_updated_at = pharmacy.updated_at

        mask = PurchaseRepo.get_mask(db, mask_id, pharmacy_id)
        if not mask:
            raise HTTPException(status_code=404, detail="Mask not found in this pharmacy")

        total_price = mask.price * quantity
        if user.cash_balance < total_price:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        user.cash_balance -= total_price
        user.updated_at = datetime.now(timezone.utc)

        pharmacy.cash_balance += total_price
        pharmacy.updated_at = datetime.now(timezone.utc)

        purchase_history = PurchaseHistory(
            user_id=user.id,
            pharmacy_name=pharmacy.name,
            mask_name=mask.name,
            transaction_amount=total_price,
            transaction_date=int(datetime.now(timezone.utc).timestamp())
        )

        PurchaseRepo.create_purchase_history(db, purchase_history)

        # Optimistic Locking compare updated_at
        affected_rows = PurchaseRepo.update_user_balance(db, user, user_prev_updated_at)
        affected_pharmacies = PurchaseRepo.update_pharmacy_balance(db, pharmacy, pharmacy_prev_updated_at)

        if affected_rows == 0 or affected_pharmacies == 0:
            db.rollback()
            raise HTTPException(status_code=409, detail="Transaction conflict, please retry.")

        # Submit transaction
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(status_code=409, detail="Transaction conflict, please retry.")

        return {
            "message": "Purchase successful",
            "transaction": {
                "id": purchase_history.id,
                "user_id": purchase_history.user_id,
                "pharmacy_name": purchase_history.pharmacy_name,
                "mask_name": purchase_history.mask_name,
                "transaction_amount": purchase_history.transaction_amount,
                "transaction_date": purchase_history.transaction_date
            },
            "user": {
                "id": user.id,
                "name": user.name,
                "cash_balance": user.cash_balance,
            },
            "pharmacy": {
                "id": pharmacy.id,
                "name": pharmacy.name,
                "cash_balance": pharmacy.cash_balance,
            }
        }
