from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from app.models.user import User
from app.models.purchase_history import PurchaseHistory

class UserRepo:
    @staticmethod
    def get_top_users_by_spending(db: Session, limit: int = 10, start_date: int = None, end_date: int = None):
        """
        Query the top `limit` users with the highest purchase amount within the time range of `start_date` and `end_date`.
        """

        subquery = db.query(
            PurchaseHistory.user_id,
            func.sum(PurchaseHistory.transaction_amount).label("total_spent")
        )

        if start_date:
            subquery = subquery.filter(PurchaseHistory.transaction_date >= start_date)
        if end_date:
            subquery = subquery.filter(PurchaseHistory.transaction_date <= end_date)

        subquery = subquery.group_by(PurchaseHistory.user_id).subquery()
        
        query = (
            db.query(
                User.id,
                User.name,
                User.cash_balance,
                subquery.c.total_spent
            )
            .join(subquery, User.id == subquery.c.user_id)
            .order_by(desc(subquery.c.total_spent))
        )
        
        users = query.limit(limit).all()
        
        return [
            {
                "id": u.id, 
                "name": u.name, 
                "total_spent": float(u.total_spent), 
                "cash_balance": u.cash_balance
            } for u in users
        ]