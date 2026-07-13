from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from my_app.models.product import Product
from my_app.models.order import Order
from my_app.services.audit_service import AuditService


class SmartInventoryService:

    @staticmethod
    def low_stock_alerts(db: Session, threshold: int = 10):
        return db.query(Product).filter(Product.stock <= threshold).all()

    @staticmethod
    def predict_depletion(db: Session, product_id: int):
        """
        Predict when stock will hit zero based on average daily sales.
        """
        # Get product
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None

        # Get daily sales
        daily_sales = (
            db.query(func.sum(Order.quantity))
            .filter(Order.product_id == product_id)
            .group_by(func.date(Order.created_at))
            .all()
        )

        if not daily_sales:
            return {"prediction": "No sales history"}

        avg_daily_sales = sum([x[0] for x in daily_sales]) / len(daily_sales)

        if avg_daily_sales == 0:
            return {"prediction": "No depletion expected"}

        days_left = product.stock / avg_daily_sales
        depletion_date = datetime.utcnow() + timedelta(days=days_left)

        return {
            "product_id": product_id,
            "stock": product.stock,
            "avg_daily_sales": avg_daily_sales,
            "days_left": round(days_left, 2),
            "predicted_depletion": depletion_date.isoformat()
        }

    @staticmethod
    def auto_restock(db: Session, threshold: int = 10, restock_to: int = 50):
        """
        Auto-restock any product below threshold.
        """
        products = db.query(Product).filter(Product.stock < threshold).all()
        restocked = []

        for p in products:
            old_stock = p.stock
            p.stock = restock_to
            db.commit()
            db.refresh(p)

            AuditService.log(
                db,
                action="auto_restock",
                username="system",
                details=f"Auto-restocked {p.name} from {old_stock} to {restock_to}"
            )

            restocked.append(p)

        return restocked

    @staticmethod
    def inventory_trends(db: Session):
        """
        Returns stock levels over time based on order history.
        """
        products = db.query(Product).all()
        trends = {}

        for p in products:
            sales = (
                db.query(func.date(Order.created_at).label("day"),
                         func.sum(Order.quantity).label("qty"))
                .filter(Order.product_id == p.id)
                .group_by(func.date(Order.created_at))
                .order_by(func.date(Order.created_at))
                .all()
            )

            trends[p.name] = [
                {"day": s.day, "sold": s.qty}
                for s in sales
            ]

        return trends
