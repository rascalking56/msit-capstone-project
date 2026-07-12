from pydantic import BaseModel
from datetime import datetime


class RefreshTokenResponse(BaseModel):
    id: int
    token: str
    username: str
    revoked: bool
    created_at: datetime
    expires_at: datetime

    class Config:
        orm_mode = True
