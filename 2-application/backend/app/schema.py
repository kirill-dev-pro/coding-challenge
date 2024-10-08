from pydantic import BaseModel
from datetime import datetime


class OrderCreate(BaseModel):
    user_id: int
    product: str
    quantity: int
    total_price: float


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product: str
    quantity: int
    total_price: float
    order_date: datetime
