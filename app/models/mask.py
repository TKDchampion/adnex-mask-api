from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Mask(Base):
    __tablename__ = "masks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))

    # The mask belongs to a pharmacy
    pharmacy = relationship("Pharmacy", back_populates="masks")
