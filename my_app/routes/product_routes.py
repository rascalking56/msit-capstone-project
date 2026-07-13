from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.models.product import Product
from my_app.auth.auth_handler import require_role
from my_app.services.audit_service import AuditService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", dependencies=[Depends(require_role(["admin"]))])
def create_product(payload: dict, db: Session = Depends(get_db)):
    name = payload.get("name")
    price = payload.get("price")
    stock = payload.get("stock", 0)

    if db.query(Product).filter(Product.name == name).first():
        raise HTTPException(status_code=400, detail="Product name already exists")

    product = Product(name=name, price=price, stock=stock)
    db.add(product)
    db.commit()
    db.refresh(product)

    AuditService.log(db, action="create_product", username="admin", details=f"Created product {name}")

    return {"message": "Product created", "product": product}


@router.put("/{product_id}", dependencies=[Depends(require_role(["admin"]))])
def update_product(product_id: int, payload: dict, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = payload.get("name", product.name)
    product.price = payload.get("price", product.price)
    product.stock = payload.get("stock", product.stock)

    db.commit()
    db.refresh(product)

    AuditService.log(db, action="update_product", username="admin", details=f"Updated product {product_id}")

    return {"message": "Product updated", "product": product}


@router.delete("/{product_id}", dependencies=[Depends(require_role(["admin"]))])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    AuditService.log(db, action="delete_product", username="admin", details=f"Deleted product {product_id}")

    return {"message": "Product deleted"}
