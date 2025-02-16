from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    name: str
    cash_balance: float

class UserTopResponse(UserBase):
    total_spent: float

    class Config:
        from_attributes = True