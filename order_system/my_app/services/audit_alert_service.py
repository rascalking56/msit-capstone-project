from sqlalchemy.orm import Session
from my_app.models.product import Product
from my_app.models.audit_log import AuditLog
from datetime import datetime, timedelta


class AuditAlertService:

    @staticmethod
    def low_stock_alerts(db: Session, threshold: int = 5):
        low_stock = db.query(Product).filter(Product.stock < threshold).all()
        return [
            {
                "product_id": p.id,
                "name": p.name,
                "stock": p.stock,
                "alert": "LOW_STOCK"
            }
            for p in low_stock
        ]

    @staticmethod
    def failed_login_alerts(db: Session, minutes: int = 30):
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)
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
