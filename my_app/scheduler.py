from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from my_app.database import SessionLocal
from my_app.services.audit_service import AuditService
from my_app.services.smart_inventory_service import SmartInventoryService
from my_app.models.order import Order
from my_app.services.notification_service import NotificationService


def nightly_audit_summary():
    db = SessionLocal()
    logs = db.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 50").fetchall()

    summary = "<h3>Nightly Audit Summary</h3><ul>"
    for log in logs:
        summary += f"<li>{log.timestamp}: {log.action} — {log.username}</li>"
    summary += "</ul>"

    NotificationService.send_email(
        to_email="admin@example.com",
        subject="Nightly Audit Summary",
        message=summary
    )

    db.close()


def daily_inventory_check():
    db = SessionLocal()
    low_stock = SmartInventoryService.low_stock_alerts(db)

    if low_stock:
        msg = "<h3>Daily Inventory Check</h3><ul>"
        for p in low_stock:
            msg += f"<li>{p.name}: {p.stock} left</li>"
        msg += "</ul>"

        NotificationService.send_email(
            to_email="admin@example.com",
            subject="Daily Inventory Alert",
            message=msg
        )

    db.close()


def auto_archive_old_orders():
    db = SessionLocal()
    cutoff = datetime.utcnow() - timedelta(days=30)

    old_orders = db.query(Order).filter(Order.created_at <= cutoff).all()

    for order in old_orders:
        order.status = "archived"

    db.commit()

    if old_orders:
        NotificationService.send_email(
            to_email="admin@example.com",
            subject="Order Archive Report",
            message=f"{len(old_orders)} orders archived."
        )

    db.close()


def weekly_admin_report():
    db = SessionLocal()

    # Count orders
    total_orders = db.query(Order).count()

    # Count low stock
    low_stock = len(SmartInventoryService.low_stock_alerts(db))

    # Count audit logs
    audit_count = db.execute("SELECT COUNT(*) FROM audit_logs").scalar()

    report = f"""
    <h3>Weekly Admin Report</h3>
    <p>Total Orders: {total_orders}</p>
    <p>Low Stock Items: {low_stock}</p>
    <p>Total Audit Logs: {audit_count}</p>
    """

    NotificationService.send_email(
        to_email="admin@example.com",
        subject="Weekly Admin Report",
        message=report
    )

    db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()

    # Nightly audit summary at 2 AM
    scheduler.add_job(nightly_audit_summary, "cron", hour=2, minute=0)

    # Daily inventory check at 3 AM
    scheduler.add_job(daily_inventory_check, "cron", hour=3, minute=0)

    # Auto archive old orders at 4 AM
    scheduler.add_job(auto_archive_old_orders, "cron", hour=4, minute=0)

    # Weekly admin report every Monday at 8 AM
    scheduler.add_job(weekly_admin_report, "cron", day_of_week="mon", hour=8, minute=0)

    scheduler.start()
