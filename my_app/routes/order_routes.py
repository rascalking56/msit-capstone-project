from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.models.order import Order
from my_app.models.product import Product
from my_app.auth.auth_handler import require_role
from my_app.services.audit_service import AuditService

router = APIRouter(prefix="/orders", tags=["Orders"])


# ---------------------------------------------------------
# Create Order (Customer Only)
# ---------------------------------------------------------
@router.post("/", dependencies=[Depends(require_role(["customer"]))])
def create_order(payload: dict,
                 credentials=Depends(require_role(["customer"])),
                 db: Session = Depends(get_db)):

    username = credentials["sub"]
    product_id = payload.get("product_id")
    quantity = payload.get("quantity")

    if quantity is None or quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    # Reduce stock
    product.stock -= quantity

    order = Order(
        product_id=product_id,
        quantity=quantity,
        customer_username=username,
        status="pending"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    # Audit log
    AuditService.log(
        db=db,
        action="create_order",
        username=username,
        details=f"Ordered {quantity} of {product.name}"
    )

    return {"message": "Order created", "order": order}


# ---------------------------------------------------------
# Get All Orders (Admin + Staff)
# ---------------------------------------------------------
@router.get("/", dependencies=[Depends(require_role(["admin", "staff"]))])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


# ---------------------------------------------------------
# Get Single Order (Admin + Staff + Customer)
# ---------------------------------------------------------
@router.get("/{order_id}", dependencies=[Depends(require_role(["admin", "staff", "customer"]))])
def get_order(order_id: int,
              credentials=Depends(require_role(["admin", "staff", "customer"])),
              db: Session = Depends(get_db)):

    username = credentials["sub"]
    role = credentials["role"]

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Customers can only view their own orders
    if role == "customer" and order.customer_username != username:
        raise HTTPException(status_code=403, detail="Forbidden: This order does not belong to you")

    return order


# ---------------------------------------------------------
# Customer: My Orders
# ---------------------------------------------------------
@router.get("/my", dependencies=[Depends(require_role(["customer"]))])
def my_orders(credentials=Depends(require_role(["customer"])),
              db: Session = Depends(get_db)):

    username = credentials["sub"]
    orders = db.query(Order).filter(Order.customer_username == username).all()
    return orders


# ---------------------------------------------------------
# Update Order Status (Admin + Staff)
# ---------------------------------------------------------
@router.put("/{order_id}/status", dependencies=[Depends(require_role(["admin", "staff"]))])
def update_status(order_id: int, payload: dict, db: Session = Depends(get_db)):
    new_status = payload.get("status")

    if not new_status:
        raise HTTPException(status_code=400, detail="Status is required")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    old_status = order.status
    order.status = new_status

    db.commit()
    db.refresh(order)

    # Audit log
    AuditService.log(
        db=db,
        action="update_order_status",
        username="system",
        details=f"Order {order_id} status changed from {old_status} to {new_status}"
    )

    return {"message": "Status updated", "order": order}


# ---------------------------------------------------------
# Delete Order (Admin Only)
# ---------------------------------------------------------
@router.delete("/{order_id}", dependencies=[Depends(require_role(["admin"]))])
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    # Audit log
    AuditService.log(
        db=db,
        action="delete_order",
        username="admin",
        details=f"Deleted order {order_id}"
    )

    return {"message": "Order deleted"}
