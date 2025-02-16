from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.purchase_service import PurchaseService
from app.views.purchase_histories_schema import PurchaseTransactionResponse

router = APIRouter()

@router.post("/purchase", response_model=PurchaseTransactionResponse)
def purchase_mask(
    user_id: int,
    pharmacy_id: int,
    mask_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    """
    Mask purchase based on ACID rules
    """
    return PurchaseService.process_purchase(db, user_id, pharmacy_id, mask_id, quantity)
