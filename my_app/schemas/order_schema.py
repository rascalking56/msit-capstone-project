from datetime import datetime
from pydantic import BaseModel


# ---------------------------------------------------------
# BASE ORDER SCHEMA
# ---------------------------------------------------------
class OrderBase(BaseModel):
    product: str
    quantity: int
    price: float
    status: str | None = "pending"
    customer_name: str | None = "Unknown"


# ---------------------------------------------------------
# ORDER CREATE SCHEMA
# ---------------------------------------------------------
class OrderCreate(OrderBase):
    pass


# ---------------------------------------------------------
# ORDER UPDATE SCHEMA
# ---------------------------------------------------------
class OrderUpdate(BaseModel):
    product: str | None = None
    quantity: int | None = None
    price: float | None = None
    status: str | None = None
    customer_name: str | None = None


# ---------------------------------------------------------
# ORDER RESPONSE SCHEMA
# ---------------------------------------------------------
class OrderResponse(OrderBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    total: float

    class Config:
        orm_mode = True
