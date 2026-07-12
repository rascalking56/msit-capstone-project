from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from my_app.database import SessionLocal
from my_app.models.audit_log import AuditLog
from my_app.auth.auth_handler import require_role
from my_app.schemas.audit_schema import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["Audit"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard", response_model=list[AuditLogResponse])
def audit_dashboard(
    payload=Depends(require_role(["admin", "staff"])),
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(50).all()
    return logs
