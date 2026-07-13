from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.models.user import User
from my_app.auth.password_utils import verify_password
from my_app.auth.auth_handler import (
    create_access_token,
    create_refresh_token,
    require_role
)
from my_app.services.audit_service import AuditService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ---------------------------------------------------------
# Unified Login (Admin, Staff, Customer)
# ---------------------------------------------------------
@router.post("/login")
def login(payload: dict, request: Request, db: Session = Depends(get_db)):
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    # Fetch user from DB
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Verify password
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Role comes directly from DB: admin, staff, customer
    role = user.role

    # Device + session metadata
    device_id = payload.get("device_id", "unknown-device")
    user_agent = request.headers.get("user-agent", "unknown")
    ip = request.client.host

    # Generate tokens
    access_token = create_access_token(username, role)
    refresh_token = create_refresh_token(username, device_id, user_agent, ip)

    # Audit log
    AuditService.log(
        db=db,
        action="login",
        username=username,
        details=f"Role={role}, IP={ip}, Device={device_id}"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": role,
        "token_type": "bearer"
    }


# ---------------------------------------------------------
# Refresh Access Token
# ---------------------------------------------------------
@router.post("/refresh")
def refresh_token(payload: dict,
                  request: Request,
                  db: Session = Depends(get_db)):

    refresh_token = payload.get("refresh_token")
    device_id = payload.get("device_id", "unknown-device")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    # Validate refresh token
    session = db.query(User).filter(User.refresh_token == refresh_token).first()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    username = session.username
    role = session.role

    user_agent = request.headers.get("user-agent", "unknown")
    ip = request.client.host

    # Issue new access token
    new_access_token = create_access_token(username, role)

    # Audit log
    AuditService.log(
        db=db,
        action="refresh_token",
        username=username,
        details=f"IP={ip}, Device={device_id}"
    )

    return {
        "access_token": new_access_token,
        "role": role,
        "token_type": "bearer"
    }


# ---------------------------------------------------------
# Protected Route Example (Admin Only)
# ---------------------------------------------------------
@router.get("/admin-check", dependencies=[Depends(require_role(["admin"]))])
def admin_check(credentials=Depends(require_role(["admin"]))):
    return {"message": "Admin access verified", "user": credentials["sub"]}


# ---------------------------------------------------------
# Protected Route Example (Staff Only)
# ---------------------------------------------------------
@router.get("/staff-check", dependencies=[Depends(require_role(["staff"]))])
def staff_check(credentials=Depends(require_role(["staff"]))):
    return {"message": "Staff access verified", "user": credentials["sub"]}


# ---------------------------------------------------------
# Protected Route Example (Customer Only)
# ---------------------------------------------------------
@router.get("/customer-check", dependencies=[Depends(require_role(["customer"]))])
def customer_check(credentials=Depends(require_role(["customer"]))):
    return {"message": "Customer access verified", "user": credentials["sub"]}
