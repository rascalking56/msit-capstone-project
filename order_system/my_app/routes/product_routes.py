from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.models.product import Product
from my_app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from my_app.auth.auth_handler import require_role

router = APIRouter(prefix="/products", tags=["Products"])


# -----------------------------
# Create Product (Admin Only)
# -----------------------------
@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    existing = db.query(Product).filter(Product.name == product.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists"
        )

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        created_by=payload["sub"],
        role_created=payload["role"]
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# -----------------------------
# Get All Products (Everyone)
# -----------------------------
@router.get("/", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


# -----------------------------
# Get Single Product (Everyone)
# -----------------------------
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


# -----------------------------
# Update Product (Admin + Staff)
# -----------------------------
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    update_data: ProductUpdate,
    payload=Depends(require_role(["admin", "staff"])),
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
        product.stock = update_data.stock

    db.commit()
    db.refresh(product)

    return product


# -----------------------------
# Delete Product (Admin Only)
# -----------------------------
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {"message": f"Product {product_id} deleted successfully"}
