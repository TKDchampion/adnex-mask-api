from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.pharmacy import Pharmacy
from app.models.mask import Mask

class SearchRepo:
    @staticmethod
    def search_pharmacies_and_masks(db: Session, query: str):
        """
        Fuzzy search for `pharmacies.name` or `masks.name`
        - Use `ILIKE` for broad matching
        - Use `similarity()` to rank by relevance
        """

        search_term = f"%{query}%"

        pharmacy_results = (
            db.query(
                Pharmacy.id, 
                Pharmacy.name, 
                Pharmacy.cash_balance, 
                func.similarity(Pharmacy.name, query).label("similarity"))
            .filter(Pharmacy.name.ilike(search_term))
            .order_by(desc("similarity"))
            .all()
        )

        mask_results = (
            db.query(
                Mask.id, 
                Mask.name, 
                Mask.pharmacy_id, 
                Mask.price,func.similarity(Mask.name, query).label("similarity"))
            .filter(Mask.name.ilike(search_term))
            .order_by(desc("similarity"))
            .all()
        )

        return {
            "pharmacies": [{
                "id": p.id, 
                "name": p.name, 
                "similarity": p.similarity, 
                "cash_balance": p.cash_balance} for p in pharmacy_results],
            "masks": [{
                "id": m.id, 
                "name": m.name, 
                "price": m.price, 
                "pharmacy_id": m.pharmacy_id, 
                "similarity": m.similarity} for m in mask_results]
        }
