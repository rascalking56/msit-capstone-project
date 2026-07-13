from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from my_app.database import SessionLocal
from my_app.models.audit_log import AuditLog
from my_app.auth.auth_handler import require_role

router = APIRouter(prefix="/admin/audit", tags=["Audit"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_audit_logs(
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
    return logs
