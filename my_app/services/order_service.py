from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from my_app.models.order import Order


class OrderService:

    @staticmethod
    def create_order(db: Session, data, username: str, role: str):
        order = Order(
            customer_name=data.customer_name,
            item_name=data.item_name,
            quantity=data.quantity,
            status="pending",
            created_by=username,
            role_created=role
        )

        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def update_status(db: Session, order_id: int, new_status: str):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        order.status = new_status
        db.commit()
        db.refresh(order)
        return order
