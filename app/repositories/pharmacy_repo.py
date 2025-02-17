from datetime import datetime
from sqlalchemy import and_, exists, func
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
    def get_pharmacies_with_masks_and_hours(
        db: Session, 
        mask_count: int, 
        min_price: float, 
        max_price: float,
        day: str = None, 
        time: str = None
    ):
        """
        Get pharmacies that:
        - Have masks within a price range.
        - Have at least `mask_count` masks.
        - Are open on the given `day` and `time` (if provided).
        """
        filtered_masks = db.query(Mask).filter(
            Mask.price >= min_price,
            Mask.price <= max_price
        ).subquery()

        mask_count_subquery = (
            db.query(
                filtered_masks.c.pharmacy_id,
                func.count(filtered_masks.c.id).label("mask_count"),
                func.json_agg(
                    func.json_build_object(
                        "id", filtered_masks.c.id,
                        "name", filtered_masks.c.name,
                        "price", filtered_masks.c.price
                    )
                ).label("masks")
            )
            .group_by(filtered_masks.c.pharmacy_id)
            .having(func.count(filtered_masks.c.id) >= mask_count)
            .subquery()
        )

        final_query = db.query(
            Pharmacy.id,
            Pharmacy.name,
            Pharmacy.cash_balance,
            mask_count_subquery.c.masks
        ).join(mask_count_subquery, Pharmacy.id == mask_count_subquery.c.pharmacy_id)

        if day or time:
            conditions = []
            if day:
                conditions.append(BusinessHours.weekday == day)
            if time:
                try:
                    time_obj = datetime.strptime(time, "%H:%M").time()
                    conditions.append(and_(
                        BusinessHours.open_time <= time_obj,
                        BusinessHours.close_time > time_obj
                    ))
                except ValueError:
                    raise ValueError("Invalid time format. Expected HH:MM.")

            final_query = final_query.filter(
                exists().where(
                    and_(
                        BusinessHours.pharmacy_id == Pharmacy.id,
                        *conditions
                    )
                )
            )
            
        return final_query