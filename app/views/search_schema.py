from pydantic import BaseModel
from typing import List

from app.views.mask_schema import MaskSimilarity
from app.views.pharmacy_schema import PharmacySimilarity

class SearchResponse(BaseModel):
    pharmacies: List[PharmacySimilarity]
    masks: List[MaskSimilarity]

    class Config:
        from_attributes = True