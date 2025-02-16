from pydantic import BaseModel

class MaskBase(BaseModel):
    id: int
    name: str
    price: float

class MaskResponse(MaskBase):    
    class Config:
        from_attributes = True
        
class MaskSimilarity(MaskBase):
    similarity: float
    pharmacy_id: int