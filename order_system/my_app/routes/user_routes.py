from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from my_app.database import SessionLocal
from my_app.models.user import User
from my_app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from my_app.auth.auth_handler import (
    hash_password,
    verify_password,
    create_access_token,
    require_role,
)

router = APIRouter(prefix="/users", tags=["Users"])


# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Register User
# -----------------------------
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    hashed_pw = get_password_hash(user.password)

    new_user = User(
        username=user.username,
        hashed_password=hashed_pw,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -----------------------------
# Login User
# -----------------------------
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    token = create_access_token({
        "sub": db_user.username,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role
    }


# -----------------------------
# Protected Route (Any Role)
# -----------------------------
@router.get("/protected")
def protected_route(payload = Depends(require_role(["admin", "staff", "customer"]))):
    return {
        "message": "Protected route accessed",
        "user": payload["sub"],
        "role": payload["role"]
    }


# -----------------------------
# Admin-Only Route
# -----------------------------
@router.get("/admin-only")
def admin_only(payload = Depends(require_role(["admin"]))):
    return {
        "message": "Admin access granted",
        "user": payload["sub"],
        "role": payload["role"]
    }


# -----------------------------
# Staff + Admin Route
# -----------------------------
@router.get("/staff-area")
def staff_area(payload = Depends(require_role(["admin", "staff"]))):
    return {
        "message": "Staff/Admin access granted",
        "user": payload["sub"],
        "role": payload["role"]
    }


# -----------------------------
# Customer Route
# -----------------------------
@router.get("/customer-area")
def customer_area(payload = Depends(require_role(["customer"]))):
    return {
        "message": "Customer access granted",
        "user": payload["sub"],
        "role": payload["role"]
    }