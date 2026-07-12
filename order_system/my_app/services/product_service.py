from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from my_app.models.product import Product


class ProductService:

    @staticmethod
    def create_product(db: Session, data, username: str, role: str):
        existing = db.query(Product).filter(Product.name == data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already exists"
            )

        product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            stock=data.stock,
            created_by=username,
            role_created=role
        )

        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update_product(db: Session, product_id: int, data):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        if data.name is not None:
            product.name = data.name
        if data.description is not None:
            product.description = data.description
        if data.price is not None:
            product.price = data.price
        if data.stock is not None:
            if data.stock < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Stock cannot be negative"
                )
            product.stock = data.stock

        db.commit()
        db.refresh(product)
        return product
