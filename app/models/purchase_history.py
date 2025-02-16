from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class PurchaseHistory(Base):
    __tablename__ = "purchase_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pharmacy_name = Column(String, nullable=False)
    mask_name = Column(String, nullable=False)
    transaction_amount = Column(Float, nullable=False)
    transaction_date = Column(Integer, nullable=False)

    # The purchase_histories to a User
    user = relationship("User", back_populates="purchase_histories")
