from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from my_app.database import SessionLocal
from my_app.services.alert_service import AlertService
from my_app.auth.auth_handler import require_role

router = APIRouter(prefix="/alerts", tags=["Alerts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/low-stock")
def low_stock_alerts(
    payload=Depends(require_role(["admin", "staff"])),
    db: Session = Depends(get_db)
):
    return AlertService.low_stock(db)


@router.get("/failed-logins")
def failed_login_alerts(
    payload=Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    return AlertService.failed_logins(db)
