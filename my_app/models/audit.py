from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from my_app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, nullable=False)
    action = Column(String, nullable=False)
    details = Column(String, nullable=True)   # ✔ REQUIRED
    timestamp = Column(DateTime, default=datetime.utcnow)
