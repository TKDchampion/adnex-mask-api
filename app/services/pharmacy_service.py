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
        """
        Filter pharmacies：
            - `mask_count`：Filter pharmacies that have at least X masks
            - `min_price`、`max_price`：Mask price range
            - `day`、`time`：Filter business hours
            - If none of them are provided, return all pharmacies
        """
        pharmacies = PharmacyRepo.get_pharmacies(db)

        if mask_count > 0 or min_price > 0 or max_price < 9999999.99:
            pharmacies = PharmacyRepo.get_pharmacies_with_masks(db, mask_count, min_price, max_price)

        if day:
            pharmacies = PharmacyRepo.get_pharmacies_by_business_hours(db, day, time)

        result = []
        for p in pharmacies:
            filtered_masks = [
                {"id": m.id, "name": m.name, "price": m.price,}
                for m in p.masks
                if min_price <= m.price <= max_price
            ]

            if len(filtered_masks) < mask_count:
                continue

            result.append({
                "id": p.id,
                "name": p.name,
                "cash_balance": p.cash_balance,
                "masks": filtered_masks
            })

        return result
