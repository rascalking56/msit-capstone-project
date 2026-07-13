from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.models.product import Product
from my_app.auth.auth_handler import require_role
from my_app.services.audit_service import AuditService

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/all")
def get_all_inventory(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.post("/restock/{product_id}", dependencies=[Depends(require_role(["admin", "staff"]))])
def restock(product_id: int, amount: int, db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.stock += amount
    db.commit()
    db.refresh(product)

    AuditService.log(
        db,
        action="restock",
        username="staff",
        details=f"Restocked {amount} of {product.name}",
    )

    return {"message": "Restocked", "new_stock": product.stock}


@router.post("/reduce/{product_id}", dependencies=[Depends(require_role(["admin", "staff"]))])
def reduce(product_id: int, amount: int, db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < amount:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    product.stock -= amount
    db.commit()
    db.refresh(product)

    AuditService.log(
        db,
        action="reduce_stock",
        username="staff",
        details=f"Reduced {amount} of {product.name}",
    )

    return {"message": "Reduced", "new_stock": product.stock}


@router.put("/set/{product_id}", dependencies=[Depends(require_role(["admin"]))])
def set_stock(product_id: int, new_stock: int, db: Session = Depends(get_db)):
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.stock = new_stock
    db.commit()
    db.refresh(product)

    AuditService.log(
        db,
        action="set_stock",
        username="admin",
        details=f"Set stock of {product.name} to {new_stock}",
    )

    return {"message": "Stock updated", "new_stock": product.stock}
