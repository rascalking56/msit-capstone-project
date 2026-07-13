from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from my_app.database import SessionLocal
from my_app.models.user import User
from my_app.models.order import Order
from my_app.models.product import Product
from my_app.schemas.user_schema import UserCreate, UserResponse
from my_app.auth.auth_handler import get_password_hash, require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


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
# Get All Users (Admin Only)
# -----------------------------
@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users


# -----------------------------
# Create User With Any Role (Admin Only)
# -----------------------------
@router.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
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
# Update User Role (Admin Only)
# -----------------------------
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_role(
    user_id: int,
    new_role: str,
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.role = new_role
    db.commit()
    db.refresh(user)

    return user


# -----------------------------
# Delete User (Admin Only)
# -----------------------------
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": f"User {user_id} deleted successfully"}


# -----------------------------
# View All Orders (Admin Only)
# -----------------------------
@router.get("/orders")
def admin_view_orders(
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).all()
    return orders


# -----------------------------
# View All Products (Admin Only)
# -----------------------------
@router.get("/products")
def admin_view_products(
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()
    return products


# -----------------------------
# System Audit Log (Admin Only)
# -----------------------------
@router.get("/audit")
def system_audit_log(
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).all()
    products = db.query(Product).all()

    return {
        "orders_created": [
            {
                "id": o.id,
                "item": o.item_name,
                "quantity": o.quantity,
                "created_by": o.created_by,
                "role_created": o.role_created,
                "created_at": o.created_at
            }
            for o in orders
        ],
        "products_created": [
            {
                "id": p.id,
                "name": p.name,
                "stock": p.stock,
                "created_by": p.created_by,
                "role_created": p.role_created,
                "created_at": p.created_at
            }
            for p in products
        ]
    }