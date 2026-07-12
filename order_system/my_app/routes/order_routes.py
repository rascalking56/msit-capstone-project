from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.models.order import Order
from my_app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse
from my_app.auth.auth_handler import require_role
from my_app.services.audit_service import AuditService

router = APIRouter(prefix="/orders", tags=["Orders"])


# -----------------------------
# Create Order (Admin + Staff)
# -----------------------------
@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    payload=Depends(require_role(["admin", "staff"])),
    db: Session = Depends(get_db)
):
    new_order = Order(
        product_id=order.product_id,
        quantity=order.quantity,
        created_by=payload["sub"],
        role_created=payload["role"]
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Audit log
    AuditService.log(
        db=db,
        user=payload["sub"],
        action="order_created",
        before=None,
        after=new_order.to_dict()
    )

    return new_order


# -----------------------------
# Get All Orders (Everyone)
# -----------------------------
@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


# -----------------------------
# Update Order (Admin + Staff)
# -----------------------------
@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    update_data: OrderUpdate,
    payload=Depends(require_role(["admin", "staff"])),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    before = order.to_dict()

    if update_data.quantity is not None:
        order.quantity = update_data.quantity

    db.commit()
    db.refresh(order)

    # Audit log
    AuditService.log(
        db=db,
        user=payload["sub"],
        action="order_updated",
        before=before,
        after=order.to_dict()
    )

    return order


# -----------------------------
# Delete Order (Admin Only)
# -----------------------------
@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    before = order.to_dict()

    db.delete(order)
    db.commit()

    # Audit log
    AuditService.log(
        db=db,
        user=payload["sub"],
        action="order_deleted",
        before=before,
        after=None
    )

    return {"message": f"Order {order_id} deleted successfully"}
