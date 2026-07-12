from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AuditLogResponse(BaseModel):
    id: int
    username: str
    role: str
    resource_type: str
    resource_id: int
    action: str
    before: Optional[str]
    after: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
