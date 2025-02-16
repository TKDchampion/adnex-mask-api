from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.repositories.user_repo import UserRepo
from app.views.user_schema import UserTopResponse

router = APIRouter()

@router.get("/users/top", response_model=List[UserTopResponse])
def get_top_users(
    limit: Optional[int] = Query(10, description="top x users"),
    start_date: Optional[int] = Query(None, description="start time, timestamp"),
    end_date: Optional[int] = Query(None, description="end time, timestamp"),
    db: Session = Depends(get_db)
):
    """
    Query the top `limit` users with the highest purchase amount within the time range of `start_date` and `end_date`.
    """
    users = UserRepo.get_top_users_by_spending(db, limit, start_date, end_date)

    if not users:
        return []

    return  users