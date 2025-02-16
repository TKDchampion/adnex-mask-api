from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.business_hours import BusinessHours
from app.models.pharmacy import Pharmacy
from app.models.mask import Mask

class PharmacyRepo:
    @staticmethod
    def get_masks_by_pharmacy(db: Session, pharmacy_id: int, sort_by: str = "name"):
        """
        Query masks by pharmacy_id and sort by price or name
        """
        valid_sort_fields = {"name": Mask.name, "price": Mask.price}

        if sort_by not in valid_sort_fields:
            sort_by = "name"

        masks = db.query(Mask).filter(Mask.pharmacy_id == pharmacy_id).order_by(valid_sort_fields[sort_by]).all()
        return [{"id": m.id, "name": m.name, "price": m.price} for m in masks]
    
    @staticmethod
    def get_pharmacies(db: Session):
        """
        Get all pharmacies
        """
        return db.query(Pharmacy).all()

    @staticmethod
    def get_mask_count_by_pharmacy(db: Session):
        """
        Get mask count grouped by pharmacy
        """
        return (
            db.query(Mask.pharmacy_id, func.count(Mask.id).label("mask_count"))
            .group_by(Mask.pharmacy_id)
            .all()
        )

    @staticmethod
    def get_pharmacies_with_masks(db: Session, mask_count: int, min_price: float, max_price: float):
        """
        Get pharmacies that have masks within a price range
        """
        filtered_masks = db.query(Mask).filter(Mask.price >= min_price, Mask.price <= max_price).subquery()

        mask_count_subquery = (
            db.query(
                filtered_masks.c.pharmacy_id,
                func.count(filtered_masks.c.id).label("mask_count")
            )
            .group_by(filtered_masks.c.pharmacy_id)
            .having(func.count(filtered_masks.c.id) >= mask_count)
            .subquery()
        )

        return (
            db.query(Pharmacy)
            .join(mask_count_subquery, Pharmacy.id == mask_count_subquery.c.pharmacy_id)
            .all()
        )

    @staticmethod
    def get_pharmacies_by_business_hours(db: Session, day: str, time: str = None):
        """
        Get pharmacies based on business hours
        """
        query = db.query(Pharmacy).join(BusinessHours, Pharmacy.id == BusinessHours.pharmacy_id)
        query = query.filter(BusinessHours.weekday == day)

        if time:
            query = query.filter(BusinessHours.open_time <= time, BusinessHours.close_time >= time)

        return query.distinct().all()