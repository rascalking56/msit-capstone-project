from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# -----------------------------
# Product Creation Schema
# -----------------------------
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int


# -----------------------------
# Product Update Schema
# -----------------------------
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


# -----------------------------
# Product Response Schema
# -----------------------------
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    created_by: str
    role_created: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
