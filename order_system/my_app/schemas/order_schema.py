from pydantic import BaseModel
from datetime import datetime


# -----------------------------
# Order Creation Schema
# -----------------------------
class OrderCreate(BaseModel):
    customer_name: str
    item_name: str
    quantity: int


# -----------------------------
# Order Update Schema
# -----------------------------
class OrderUpdate(BaseModel):
    status: str   # pending, processing, completed, cancelled


# -----------------------------
# Order Response Schema
# -----------------------------
class OrderResponse(BaseModel):
    id: int
    customer_name: str
    item_name: str
    quantity: int
    status: str
    created_by: str
    role_created: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
