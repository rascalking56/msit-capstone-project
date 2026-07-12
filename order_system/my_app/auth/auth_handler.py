import time
from typing import Optional

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from passlib.context import CryptContext
import jwt

# -----------------------------
# Security Configuration
# -----------------------------
SECRET_KEY = "b9f3c1e7a4d2f8c6b1e9d4f2a7c3e8b6"   # 32+ bytes, secure
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


# -----------------------------
# Password Hashing
# -----------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -----------------------------
# JWT Creation
# -----------------------------
def create_access_token(username: str, role: str) -> str:
    expire = time.time() + ACCESS_TOKEN_EXPIRE_SECONDS

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# -----------------------------
# JWT Decoding
# -----------------------------
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


# -----------------------------
# Role-Based Authorization
# -----------------------------
def require_role(allowed_roles: list):
    """
    Example:
    @router.get("/admin")
    def admin_route(payload = Depends(require_role(["admin"]))):
        return {"message": "Admin access granted"}
    """

    def role_checker(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        payload = decode_token(token)

        user_role = payload.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return payload

    return role_checker
