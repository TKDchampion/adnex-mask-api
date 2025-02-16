from sqlalchemy import Column, DateTime, Integer, String, Float, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cash_balance = Column(Float, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    purchase_histories = relationship("PurchaseHistory", back_populates="user")
