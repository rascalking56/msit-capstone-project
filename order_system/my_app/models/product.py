from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from my_app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # Product details
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    # Audit fields
    created_by = Column(String, nullable=False)      # username from JWT
    role_created = Column(String, nullable=False)    # admin or staff

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
