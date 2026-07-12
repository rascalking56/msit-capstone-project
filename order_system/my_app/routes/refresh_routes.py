from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from my_app.database import SessionLocal
from my_app.services.refresh_token_service import RefreshTokenService
from my_app.auth.auth_handler import create_access_token
from my_app.schemas.refresh_token_schema import RefreshTokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/refresh")
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    username = RefreshTokenService.verify(db, refresh_token)

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    # Rotate refresh token
    RefreshTokenService.revoke(db, refresh_token)
    new_refresh = RefreshTokenService.create(db, username)

    new_access = create_access_token({"sub": username})

    return {
        "access_token": new_access,
        "refresh_token": new_refresh.token,
        "token_type": "bearer"
    }
