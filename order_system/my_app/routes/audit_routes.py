from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.models.audit import AuditLog

router = APIRouter(prefix="/audit", tags=["Audit Logs"])


# -----------------------------
# Dashboard Endpoint (Frontend uses this)
# -----------------------------
@router.get("/dashboard")
def audit_dashboard(db: Session = Depends(get_db)):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )
    return logs


# -----------------------------
# Get All Audit Logs (Raw)
# -----------------------------
@router.get("/")
def get_all_logs(db: Session = Depends(get_db)):
    logs = (
        db.query(AuditLog)
        .order_by(AuditLog.timestamp.desc())
        .all()
    )
    return logs
