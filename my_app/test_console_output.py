"""
Test Script: Generates console output for assignment screenshots.
Runs OrderService and InventoryService functions directly.
"""

from sqlalchemy.orm import Session
from my_app.database import SessionLocal

from my_app.services.order_service import OrderService
from my_app.services.inventory_service import InventoryService
from my_app.models.product import Product


def main():
    db: Session = SessionLocal()

    print("\n==============================")
    print("  TEST: ORDER CREATION")
    print("==============================")

    # Fake request-like object for order creation
    order_data = type("obj", (object,), {
        "customer_name": "Sarah Lopez",
        "item_name": "Wireless Mouse",
        "quantity": 3
    })

    # Create order
    order = OrderService.create_order(
        db=db,
        data=order_data,
        username="admin_user",
        role="admin"
    )

    print("Order created successfully")
    print(f"Order ID: {order.id}")
    print(f"Customer: {order.customer_name}")
    print(f"Item: {order.item_name}")
    print(f"Quantity: {order.quantity}")
    print(f"Status: {order.status}")
    print(f"Created by: {order.created_by}")
    print(f"Role: {order.role_created}")

    print("\n==============================")
    print("  TEST: INVENTORY UPDATE")
    print("==============================")

    # Ensure product exists
    product = db.query(Product).filter(Product.id == 7).first()
    if not product:
        product = Product(
            id=7,
            name="Wireless Mouse",
            description="Wireless Mouse",
            price=25.99,
            stock=0,                     # REQUIRED
            created_by="admin_user",
            role_created="admin"
        )
        db.add(product)
        db.commit()
        db.refresh(product)

    # Restock inventory for product_id = 7
    inv = InventoryService.restock(
        db=db,
        product_id=7,
        amount=3,
        username="admin_user",
        role="admin"
    )

    print("Inventory updated successfully")
    print(f"Product ID: {inv.product_id}")
    print(f"New Stock: {inv.stock}")
    print(f"Updated by: {inv.created_by}")
    print(f"Role: {inv.role_created}")

    print("\n==============================")
    print("  TEST COMPLETE")
    print("==============================\n")


if __name__ == "__main__":
    main()
