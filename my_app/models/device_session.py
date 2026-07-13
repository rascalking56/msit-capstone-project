from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from my_app.database import Base


class DeviceSession(Base):
    __tablename__ = "device_sessions"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    device_id = Column(String, index=True)
    refresh_token = Column(String, unique=True)
    user_agent = Column(String)
    ip_address = Column(String)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
