from pydantic import BaseModel


class TradeCreate(BaseModel):
    user_id: int
    commodity: str
    side: str
    price: float
    lots: int


class TradeResponse(TradeCreate):
    id: int

    class Config:
        from_attributes = True
