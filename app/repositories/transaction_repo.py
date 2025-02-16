from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.purchase_history import PurchaseHistory

class TransactionRepo:
    @staticmethod
    def get_transactions(db: Session, start_date: int = None, end_date: int = None):
        """
        Get transactions within the given date range.
        """
        query = db.query(
            PurchaseHistory.id,
            PurchaseHistory.user_id,
            PurchaseHistory.transaction_amount,
            PurchaseHistory.transaction_date
        )

        if start_date:
            query = query.filter(PurchaseHistory.transaction_date >= start_date)
        if end_date:
            query = query.filter(PurchaseHistory.transaction_date <= end_date)

        return query.all()

    @staticmethod
    def get_transaction_summary(db: Session, start_date: int = None, end_date: int = None):
        """
        Get total transaction count and total amount within the given date range.
        """
        query = db.query(
            func.count(PurchaseHistory.id).label("total_transactions"),
            func.sum(PurchaseHistory.transaction_amount).label("total_amount")
        )

        if start_date:
            query = query.filter(PurchaseHistory.transaction_date >= start_date)
        if end_date:
            query = query.filter(PurchaseHistory.transaction_date <= end_date)

        return query.first()