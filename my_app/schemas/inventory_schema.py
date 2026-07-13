from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    stock: int
    created_by: str
    role_created: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
