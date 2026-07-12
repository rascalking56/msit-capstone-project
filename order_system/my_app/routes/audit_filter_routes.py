from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from my_app.database import SessionLocal
from my_app.models.audit_log import AuditLog
from my_app.schemas.audit_schema import AuditLogResponse
from my_app.auth.auth_handler import require_role

router = APIRouter(prefix="/audit/filter", tags=["Audit Filtering"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[AuditLogResponse])
def filter_audit_logs(
    username: str | None = None,
    resource_type: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    payload=Depends(require_role(["admin", "staff"])),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)

    if username:
        query = query.filter(AuditLog.username == username)

    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)

    if start_date:
        start = datetime.fromisoformat(start_date)
        query = query.filter(AuditLog.created_at >= start)

    if end_date:
        end = datetime.fromisoformat(end_date)
        query = query.filter(AuditLog.created_at <= end)

    return query.order_by(AuditLog.created_at.desc()).all()
