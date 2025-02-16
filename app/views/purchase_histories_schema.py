from typing import List
from pydantic import BaseModel

from app.views.pharmacy_schema import PharmacyBase
from app.views.user_schema import UserBase

class PurchaseHistoriesBase(BaseModel):
    id: int
    transaction_date: int
    transaction_amount: float

class PurchaseHistoriesResponse(PurchaseHistoriesBase):
    user_id: int

class PurchaseHistoriesTotalResponse(BaseModel):
    total_transactions: int
    total_amount: float
    transactions: List[PurchaseHistoriesResponse]

    class Config:
        from_attributes = True
        
class PurchaseTransaction(PurchaseHistoriesBase):
    user_id: int
    pharmacy_name: str
    mask_name: str
    
class PurchaseTransactionResponse(BaseModel):
    message: str
    transaction: PurchaseTransaction
    user: UserBase
    pharmacy: PharmacyBase
    
    class Config:
        from_attributes = True