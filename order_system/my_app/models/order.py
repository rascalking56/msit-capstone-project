from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from my_app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    # Order details
    customer_name = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    # Order status (pending, processing, completed, cancelled)
    status = Column(String, default="pending", nullable=False)

    # Audit fields
    created_by = Column(String, nullable=False)      # username from JWT
    role_created = Column(String, nullable=False)    # role from JWT

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
