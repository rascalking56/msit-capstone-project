from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from my_app.models.product import Product
from my_app.models.audit import AuditLog
from my_app.config import LOW_STOCK_THRESHOLD, FAILED_LOGIN_ALERT_WINDOW_MIN


class AlertService:

    @staticmethod
    def low_stock(db: Session):
        items = db.query(Product).filter(Product.stock < LOW_STOCK_THRESHOLD).all()
        return [
            {
                "product_id": p.id,
                "name": p.name,
                "stock": p.stock,
                "alert": "LOW_STOCK"
            }
            for p in items
        ]

    @staticmethod
    def failed_logins(db: Session):
        cutoff = datetime.utcnow() - timedelta(minutes=FAILED_LOGIN_ALERT_WINDOW_MIN)

        logs = db.query(AuditLog).filter(
            AuditLog.action == "failed_login",
            AuditLog.created_at >= cutoff
        ).all()

        return [
            {
                "username": log.username,
                "time": log.created_at,
                "alert": "FAILED_LOGIN"
            }
            for log in logs
        ]
