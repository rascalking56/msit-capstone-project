from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from my_app.models.product import Product
from my_app.models.order import Order
from my_app.models.audit import AuditLog
from my_app.services.notification_service import NotificationService


class AlertEngine:

    @staticmethod
    def low_stock_alerts(db: Session):
        products = db.query(Product).filter(Product.stock <= 10).all()
        if not products:
            return

        message = "<h3>Low Stock Alert</h3><ul>"
        for p in products:
            message += f"<li>{p.name}: {p.stock} left</li>"
        message += "</ul>"

        NotificationService.send_email(
            to_email="admin@example.com",
            subject="Low Stock Alert",
            message=message
        )

    @staticmethod
    def delayed_orders(db: Session):
        cutoff = datetime.utcnow() - timedelta(days=3)
        delayed = db.query(Order).filter(
            Order.status == "pending",
            Order.created_at <= cutoff
        ).all()

        if delayed:
            NotificationService.send_sms(
                to_number="+15555555555",
                message=f"{len(delayed)} orders delayed more than 3 days."
            )

    @staticmethod
    def new_device_login(db: Session, username: str, device_id: str):
        # Check if device seen before
        seen = db.query(AuditLog).filter(
            AuditLog.username == username,
            AuditLog.details.contains(device_id)
        ).first()

        if not seen:
            NotificationService.send_email(
                to_email=f"{username}@example.com",
                subject="New Device Login",
                message=f"Your account logged in from a new device: {device_id}"
            )

    @staticmethod
    def critical_error(message: str):
        NotificationService.send_outlook(
            to_email="admin@example.com",
            subject="Critical System Error",
            message=f"<h3>Critical Error</h3><p>{message}</p>"
        )
