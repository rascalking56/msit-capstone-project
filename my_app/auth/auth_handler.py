import secrets
from datetime import datetime, timedelta

from jose import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from my_app.database import SessionLocal
from my_app.models.device_session import DeviceSession


# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
# Generate a strong secret key once and keep it stable
SECRET_KEY = "super_secret_key_1234567890_change_me"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Must match your login route EXACTLY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ---------------------------------------------------------
# ACCESS TOKEN (short-lived)
# ---------------------------------------------------------
def create_access_token(username: str, role: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------
# REFRESH TOKEN (long-lived, device-based)
# ---------------------------------------------------------
def create_refresh_token(username: str, device_id: str, user_agent: str, ip: str):
    token = secrets.token_urlsafe(64)
    expires = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    db: Session = SessionLocal()
    session = DeviceSession(
        username=username,
        device_id=device_id,
        refresh_token=token,
        user_agent=user_agent,
        ip_address=ip,
        expires_at=expires
    )
    db.add(session)
    db.commit()
    db.close()

    return token


# ---------------------------------------------------------
# VERIFY REFRESH TOKEN
# ---------------------------------------------------------
def verify_refresh_token(token: str):
    db: Session = SessionLocal()
    session = db.query(DeviceSession).filter(DeviceSession.refresh_token == token).first()

    if not session or session.revoked:
        db.close()
        return None

    if session.expires_at < datetime.utcnow():
        session.revoked = True
        db.commit()
        db.close()
        return None

    username = session.username
    db.close()
    return username


# ---------------------------------------------------------
# REVOKE SINGLE REFRESH TOKEN
# ---------------------------------------------------------
def revoke_refresh_token(token: str):
    db: Session = SessionLocal()
    session = db.query(DeviceSession).filter(DeviceSession.refresh_token == token).first()

    if session:
        session.revoked = True
        db.commit()

    db.close()


# ---------------------------------------------------------
# REVOKE ALL SESSIONS FOR USER
# ---------------------------------------------------------
def revoke_all_sessions(username: str):
    db: Session = SessionLocal()
    sessions = db.query(DeviceSession).filter(DeviceSession.username == username).all()

    for s in sessions:
        s.revoked = True

    db.commit()
    db.close()


# ---------------------------------------------------------
# DECODE TOKEN (used by dependencies)
# ---------------------------------------------------------
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------------------------------------------------
# RBAC — REQUIRE ROLE
# ---------------------------------------------------------
def require_role(roles: list):
    def wrapper(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_role = payload.get("role")

            if user_role not in roles:
                raise HTTPException(status_code=403, detail="Forbidden")

            return payload

        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

    return wrapper
