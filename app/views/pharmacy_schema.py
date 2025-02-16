from pydantic import BaseModel
from typing import List
from app.views.mask_schema import MaskResponse

class PharmacyBase(BaseModel):
    id: int
    name: str
    cash_balance: float

class PharmacyResponse(PharmacyBase):
    masks: List[MaskResponse]

    class Config:
        from_attributes = True

class PharmacySimilarity(PharmacyBase):
    similarity: float