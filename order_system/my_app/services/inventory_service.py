from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from my_app.models.product import Product
from my_app.models.inventory import Inventory


class InventoryService:

    # -----------------------------
    # Get inventory record (or create one)
    # -----------------------------
    @staticmethod
    def get_or_create_inventory(db: Session, product_id: int, username: str, role: str):
        inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()

        if inventory:
            return inventory

        # Create new inventory record if missing
        new_inv = Inventory(
            product_id=product_id,
            stock=0,
            created_by=username,
            role_created=role
        )
        db.add(new_inv)
        db.commit()
        db.refresh(new_inv)
        return new_inv

    # -----------------------------
    # Validate product exists
    # -----------------------------
    @staticmethod
    def validate_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product

    # -----------------------------
    # Restock inventory
    # -----------------------------
    @staticmethod
    def restock(db: Session, product_id: int, amount: int, username: str, role: str):
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restock amount must be greater than zero"
            )

        InventoryService.validate_product(db, product_id)
        inventory = InventoryService.get_or_create_inventory(db, product_id, username, role)

        inventory.stock += amount
        db.commit()
        db.refresh(inventory)

        return inventory

    # -----------------------------
    # Reduce inventory
    # -----------------------------
    @staticmethod
    def reduce(db: Session, product_id: int, amount: int, username: str, role: str):
        if amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reduction amount must be greater than zero"
            )

        InventoryService.validate_product(db, product_id)
        inventory = InventoryService.get_or_create_inventory(db, product_id, username, role)

        if inventory.stock - amount < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot reduce stock below zero"
            )

        inventory.stock -= amount
        db.commit()
        db.refresh(inventory)

        return inventory

    # -----------------------------
    # Set inventory (admin only)
    # -----------------------------
    @staticmethod
    def set_stock(db: Session, product_id: int, new_stock: int, username: str, role: str):
        if new_stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock cannot be negative"
            )

        InventoryService.validate_product(db, product_id)
        inventory = InventoryService.get_or_create_inventory(db, product_id, username, role)

        inventory.stock = new_stock
        db.commit()
        db.refresh(inventory)

        return inventory

    # -----------------------------
    # Get inventory for product
    # -----------------------------
    @staticmethod
    def get_inventory(db: Session, product_id: int):
        InventoryService.validate_product(db, product_id)
        inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()

        if not inventory:
            return {"product_id": product_id, "stock": 0}

        return inventory
AuditService.log(
    db=db,
    username=username,
    role=role,
    resource_type="inventory",
    resource_id=inventory.id,
    action="restock",
    before={"stock": inventory.stock},
    after={"stock": inventory.stock + amount}
)
