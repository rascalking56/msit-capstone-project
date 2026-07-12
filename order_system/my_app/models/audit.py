from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from my_app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, nullable=False)
    action = Column(String, nullable=False)

    before_state = Column(JSON, nullable=True)
    after_state = Column(JSON, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
