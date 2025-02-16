from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.search_repo import SearchRepo
from app.views.search_schema import SearchResponse

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., description="Search keywords: Mask"),
    db: Session = Depends(get_db)
):
    """
    Fuzzy search for pharmacies.name or masks.name, sort by relevance
    """
    return SearchRepo.search_pharmacies_and_masks(db, q)
