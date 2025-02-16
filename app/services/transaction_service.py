from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.repositories.transaction_repo import TransactionRepo


class TransactionService:
    @staticmethod
    def get_transaction_summary(db: Session, start_date: int = None, end_date: int = None):
        """
        Query transactions within the time range, count the total number of transactions, 
        calculate total transaction amount, and return the matching transaction list.
        """
        transactions = TransactionRepo.get_transactions(db, start_date, end_date)
        summary = TransactionRepo.get_transaction_summary(db, start_date, end_date)

        # `summary` 可能是 SQLAlchemy Row 或 None
        if summary:
            total_transactions = summary.total_transactions if hasattr(summary, "total_transactions") else 0
            total_amount = summary.total_amount if hasattr(summary, "total_amount") else 0
        else:
            total_transactions = 0
            total_amount = 0

        transactions_data = [
            {
                "id": t.id,
                "user_id": t.user_id,
                "transaction_amount": t.transaction_amount,
                "transaction_date": t.transaction_date.isoformat() if hasattr(t.transaction_date, "isoformat") else t.transaction_date,
            }
            for t in transactions
        ]

        return jsonable_encoder({
            "total_transactions": total_transactions,
            "total_amount": total_amount,
            "transactions": transactions_data
        })
