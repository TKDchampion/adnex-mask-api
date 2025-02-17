import json
from sqlalchemy.orm import Session

from app.repositories.pharmacy_repo import PharmacyRepo


class PharmacyService:
    @staticmethod
    def get_pharmacies_by_criteria(
        db: Session,
        mask_count: int = 0,
        min_price: float = 0,
        max_price: float = 9999999.99,
        day: str = None,
        time: str = None,
    ):
        pharmacies = PharmacyRepo.get_pharmacies(db)
        
        if mask_count > 0 or min_price > 0 or max_price < 9999999.99 or day or time:
            pharmacies = PharmacyRepo.get_pharmacies_with_masks_and_hours(db, mask_count, min_price, max_price, day, time)

        return [{
                    "id": p.id,
                    "name": p.name,
                    "cash_balance": p.cash_balance,
                    "masks": json.loads(p.masks) if isinstance(p.masks, str) else p.masks or []
                } for p in pharmacies]
