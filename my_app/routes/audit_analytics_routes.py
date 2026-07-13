from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime

from my_app.database import get_db
from my_app.auth.auth_handler import require_role
from my_app.services.audit_analytics_service import AuditAnalyticsService

router = APIRouter(prefix="/audit/analytics", tags=["Audit Analytics"])


@router.get("/filter", dependencies=[Depends(require_role(["admin"]))])
def filter_logs(user: str | None = None,
                action: str | None = None,
                start: str | None = None,
                end: str | None = None,
                db: Session = Depends(get_db)):

    start_dt = datetime.fromisoformat(start) if start else None
    end_dt = datetime.fromisoformat(end) if end else None

    logs = AuditAnalyticsService.filter_logs(db, user, action, start_dt, end_dt)
    return logs


@router.get("/suspicious", dependencies=[Depends(require_role(["admin"]))])
def suspicious(db: Session = Depends(get_db)):
    return AuditAnalyticsService.suspicious_activity(db)


@router.get("/export/csv", dependencies=[Depends(require_role(["admin"]))])
def export_csv(db: Session = Depends(get_db)):
    logs = AuditAnalyticsService.filter_logs(db)
    csv_data = AuditAnalyticsService.export_csv(logs)
    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=audit_logs.csv"}
    )


@router.get("/export/json", dependencies=[Depends(require_role(["admin"]))])
def export_json(db: Session = Depends(get_db)):
    logs = AuditAnalyticsService.filter_logs(db)
    return AuditAnalyticsService.export_json(logs)
