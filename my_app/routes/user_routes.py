from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.models.user import User
from my_app.auth.password_utils import hash_password
from my_app.auth.auth_handler import require_role
from my_app.services.audit_service import AuditService

router = APIRouter(prefix="/users", tags=["Users"])


# ---------------------------------------------------------
# Register Customer
# ---------------------------------------------------------
@router.post("/register")
def register_customer(payload: dict, db: Session = Depends(get_db)):
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=username,
        password_hash=hash_password(password),
        role="customer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    AuditService.log(
        db=db,
        action="register_customer",
        user=username,   # ✔ FIXED
        details="New customer account created"
    )

    return {"message": "Customer registered", "username": username, "role": "customer"}


# ---------------------------------------------------------
# Create Staff (Admin Only)
# ---------------------------------------------------------
@router.post("/create-staff", dependencies=[Depends(require_role(["admin"]))])
def create_staff(payload: dict,
                 credentials=Depends(require_role(["admin"])),
                 db: Session = Depends(get_db)):

    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=username,
        password_hash=hash_password(password),
        role="staff"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    AuditService.log(
        db=db,
        action="create_staff",
        user=credentials["sub"],   # ✔ FIXED
        details=f"Created staff user {username}"
    )

    return {"message": "Staff created", "username": username, "role": "staff"}


# ---------------------------------------------------------
# Bootstrap Admin (First-Time Setup)
# ---------------------------------------------------------
@router.post("/bootstrap-admin")
def bootstrap_admin(db: Session = Depends(get_db)):
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        return {"message": "Admin already exists"}

    admin = User(
        username="admin",
        password_hash=hash_password("admin123"),
        role="admin"
    )

    db.add(admin)
    db.commit()

    return {
        "message": "Admin created",
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    }


# ---------------------------------------------------------
# List All Users (Admin Only)
# ---------------------------------------------------------
@router.get("/", dependencies=[Depends(require_role(["admin"]))])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# ---------------------------------------------------------
# Update User Role (Admin Only)
# ---------------------------------------------------------
@router.put("/{username}/role", dependencies=[Depends(require_role(["admin"]))])
def update_role(username: str,
                payload: dict,
                credentials=Depends(require_role(["admin"])),
                db: Session = Depends(get_db)):

    new_role = payload.get("role")
    if new_role not in ["admin", "staff", "customer"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    old_role = user.role
    user.role = new_role

    db.commit()
    db.refresh(user)

    AuditService.log(
        db=db,
        action="update_role",
        user=credentials["sub"],   # ✔ FIXED
        details=f"Changed role of {username} from {old_role} to {new_role}"
    )

    return {"message": "Role updated", "username": username, "role": new_role}


# ---------------------------------------------------------
# Delete User (Admin Only)
# ---------------------------------------------------------
@router.delete("/{username}", dependencies=[Depends(require_role(["admin"]))])
def delete_user(username: str,
                credentials=Depends(require_role(["admin"])),
                db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    AuditService.log(
        db=db,
        action="delete_user",
        user=credentials["sub"],   # ✔ FIXED
        details=f"Deleted user {username}"
    )

    return {"message": "User deleted", "username": username}
