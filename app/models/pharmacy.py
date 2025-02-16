from sqlalchemy import Column, DateTime, Integer, String, Float, func
from sqlalchemy.orm import relationship
from app.database import Base

class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cash_balance = Column(Float, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # One-to-many relationship
    masks = relationship("Mask", back_populates="pharmacy")
    business_hours = relationship("BusinessHours", back_populates="pharmacy", cascade="all, delete")
