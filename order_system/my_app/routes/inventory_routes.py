from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from my_app.database import SessionLocal
from my_app.models.product import Product
from my_app.auth.auth_handler import require_role

router = APIRouter(prefix="/inventory", tags=["Inventory"])


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
# Get Full Inventory (Everyone)
# -----------------------------
@router.get("/")
def get_inventory(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/all")
def get_all_inventory(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products




# -----------------------------
# Get Single Inventory Item (Everyone)
# -----------------------------
@router.get("/{product_id}")
def get_inventory_item(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


# -----------------------------
# Restock Product (Admin + Staff)
# -----------------------------
@router.post("/restock/{product_id}")
def restock_product(
    product_id: int,
    amount: int,
    payload=Depends(require_role(["admin", "staff"])),
    db: Session = Depends(get_db)
):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restock amount must be greater than zero"
        )

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    product.stock += amount
    db.commit()
    db.refresh(product)

    return {
        "message": f"Restocked {amount} units of {product.name}",
        "new_stock": product.stock
    }


# -----------------------------
# Reduce Stock (Admin + Staff)
# -----------------------------
@router.post("/reduce/{product_id}")
def reduce_stock(
    product_id: int,
    amount: int,
    payload=Depends(require_role(["admin", "staff"])),
    db: Session = Depends(get_db)
):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reduction amount must be greater than zero"
        )

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.stock - amount < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot reduce stock below zero"
        )

    product.stock -= amount
    db.commit()
    db.refresh(product)

    return {
        "message": f"Reduced {amount} units of {product.name}",
        "new_stock": product.stock
    }


# -----------------------------
# Set Stock (Admin Only)
# -----------------------------
@router.put("/set/{product_id}")
def set_stock(
    product_id: int,
    new_stock: int,
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    if new_stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock cannot be negative"
        )

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    product.stock = new_stock
    db.commit()
    db.refresh(product)

    return {
        "message": f"Stock for {product.name} set to {new_stock}",
        "new_stock": product.stock
    }
