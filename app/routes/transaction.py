from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.transaction_service import TransactionService
from app.views.purchase_histories_schema import PurchaseHistoriesTotalResponse

router = APIRouter()

@router.get("/transactions/summary", response_model=PurchaseHistoriesTotalResponse)
def get_transaction_summary(
    start_date: int = Query(None, description="start time (timestamp, seconds)"),
    end_date: int = Query(None, description="end time (timestamp, seconds)"),
    db: Session = Depends(get_db)
):
    """
    Calculate the number of transactions and total `transaction_amount` within the time range of `transaction_date`. 
    If not provided, calculate all transactions.
    """
    return TransactionService.get_transaction_summary(db, start_date, end_date)
