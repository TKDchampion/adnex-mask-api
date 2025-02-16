from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.pharmacy_repo import PharmacyRepo
from app.services.pharmacy_service import PharmacyService
from app.views.mask_schema import MaskResponse
from typing import List, Optional
from app.views.pharmacy_schema import PharmacyResponse

router = APIRouter()

@router.get("/pharmacies/{pharmacy_id}/masks", response_model=List[MaskResponse])
def get_masks_by_pharmacy(
    pharmacy_id: int,
    sort_by: Optional[str] = Query("name", description="sort: name or price"),
    db: Session = Depends(get_db)
):
    """
    Query masks by pharmacy_id and sort by price or name
    """
    valid_sort_fields = ["name", "price"]
    
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by: {sort_by}. Must be one of {valid_sort_fields}")

    masks = PharmacyRepo.get_masks_by_pharmacy(db, pharmacy_id, sort_by)

    if not masks:
        raise HTTPException(status_code=404, detail="No masks found for this pharmacy")

    return masks

@router.get("/pharmacies", response_model=List[PharmacyResponse])
def get_pharmacies(
    mask_count: Optional[int] = Query(0, description="At least X masks are required in the pharmacy"),
    min_price: Optional[float] = Query(0, description="Lowest mask price"),
    max_price: Optional[float] = Query(9999999.99, description="Highest mask price"),
    day: Optional[str] = Query(None, description="The name of the day of the week, such as Monday"),
    time: Optional[str] = Query(None, description="24-hour time, such as 14:00"),
    db: Session = Depends(get_db)
):
    """
    Filter pharmacies by mask quantity, price range, and opening hours
    """

    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if day and day not in valid_days:
        raise HTTPException(status_code=400, detail=f"Invalid day: {day}. Must be one of {valid_days}")

    pharmacies = PharmacyService.get_pharmacies_by_criteria(db, mask_count, min_price, max_price, day, time)

    if not pharmacies:
        return []

    return pharmacies
    