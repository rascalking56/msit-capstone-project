from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from my_app.database import SessionLocal
from my_app.models.order import Order
from my_app.models.product import Product
from my_app.schemas.order_schema import OrderResponse
from my_app.schemas.product_schema import ProductResponse, ProductUpdate
from my_app.auth.auth_handler import require_role

router = APIRouter(prefix="/staff", tags=["Staff"])


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
# Staff Dashboard (Staff + Admin)
# -----------------------------
@router.get("/dashboard")
def staff_dashboard(
    payload=Depends(require_role(["staff", "admin"])),
    db: Session = Depends(get_db)
):
    pending_orders = db.query(Order).filter(Order.status == "pending").count()
    processing_orders = db.query(Order).filter(Order.status == "processing").count()
    low_stock_items = db.query(Product).filter(Product.stock < 5).count()

    return {
        "staff_user": payload["sub"],
        "role": payload["role"],
        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "low_stock_items": low_stock_items
    }


# -----------------------------
# View All Orders (Staff + Admin)
# -----------------------------
@router.get("/orders", response_model=list[OrderResponse])
def staff_view_orders(
    payload=Depends(require_role(["staff", "admin"])),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).all()
    return orders


# -----------------------------
# Update Order Status (Staff + Admin)
# -----------------------------
@router.put("/orders/{order_id}", response_model=OrderResponse)
def staff_update_order(
    order_id: int,
    update_data: dict,
    payload=Depends(require_role(["staff", "admin"])),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    new_status = update_data.get("status")
    if not new_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status field is required"
        )

    order.status = new_status
    db.commit()
    db.refresh(order)

    return order


# -----------------------------
# View Inventory (Staff + Admin)
# -----------------------------
@router.get("/inventory", response_model=list[ProductResponse])
def staff_view_inventory(
    payload=Depends(require_role(["staff", "admin"])),
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()
    return products


# -----------------------------
# Adjust Inventory (Staff + Admin)
# -----------------------------
@router.post("/inventory/adjust/{product_id}")
def staff_adjust_inventory(
    product_id: int,
    amount: int,
    payload=Depends(require_role(["staff", "admin"])),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.stock + amount < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot reduce stock below zero"
        )

    product.stock += amount
    db.commit()
    db.refresh(product)

    return {
        "message": f"Adjusted stock for {product.name} by {amount}",
        "new_stock": product.stock
    }


# -----------------------------
# Update Product Details (Staff + Admin)
# -----------------------------
@router.put("/products/{product_id}", response_model=ProductResponse)
def staff_update_product(
    product_id: int,
    update_data: ProductUpdate,
    payload=Depends(require_role(["staff", "admin"])),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if update_data.name is not None:
        product.name = update_data.name
    if update_data.description is not None:
        product.description = update_data.description
    if update_data.price is not None:
        product.price = update_data.price
    if update_data.stock is not None:
        if update_data.stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock cannot be negative"
            )
        product.stock = update_data.stock

    db.commit()
    db.refresh(product)

    return product


# -----------------------------
# Staff Audit Log (Staff + Admin)
# -----------------------------
@router.get("/audit")
def staff_audit_log(
    payload=Depends(require_role(["staff", "admin"])),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).all()
    products = db.query(Product).all()

    return {
        "orders": [
            {
                "id": o.id,
                "item": o.item_name,
                "status": o.status,
                "created_by": o.created_by,
                "role_created": o.role_created,
                "created_at": o.created_at
            }
            for o in orders
        ],
        "products": [
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
