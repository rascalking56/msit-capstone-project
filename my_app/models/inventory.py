from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from my_app.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)

    # Link to product
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # Stock tracking
    stock = Column(Integer, nullable=False, default=0)

    # Audit fields
    created_by = Column(String, nullable=False)      # username from JWT
    role_created = Column(String, nullable=False)    # admin or staff

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    product = relationship("Product")
