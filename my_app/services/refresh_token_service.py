import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from my_app.models.refresh_token import RefreshToken
from my_app.config import REFRESH_TOKEN_EXPIRE_DAYS


class RefreshTokenService:

    @staticmethod
    def create(db: Session, username: str):
        token = secrets.token_urlsafe(64)
        expires = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        rt = RefreshToken(
            token=token,
            username=username,
            expires_at=expires
        )

        db.add(rt)
        db.commit()
        db.refresh(rt)
        return rt

    @staticmethod
    def verify(db: Session, token: str):
        rt = db.query(RefreshToken).filter(RefreshToken.token == token).first()

        if not rt or rt.revoked:
            return None

        if rt.expires_at < datetime.utcnow():
            rt.revoked = True
            db.commit()
            return None

        return rt.username

    @staticmethod
    def revoke(db: Session, token: str):
        rt = db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if rt:
            rt.revoked = True
            db.commit()
