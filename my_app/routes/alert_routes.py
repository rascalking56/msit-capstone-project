from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.auth.auth_handler import require_role
from my_app.services.alert_engine import AlertEngine

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/run", dependencies=[Depends(require_role(["admin"]))])
def run_all_alerts(db: Session = Depends(get_db)):
    AlertEngine.low_stock_alerts(db)
    AlertEngine.delayed_orders(db)
    return {"message": "Alerts executed"}


@router.post("/new-device", dependencies=[Depends(require_role(["admin", "staff"]))])
def new_device(username: str, device_id: str, db: Session = Depends(get_db)):
    AlertEngine.new_device_login(db, username, device_id)
    return {"message": "New device alert sent"}


@router.post("/critical", dependencies=[Depends(require_role(["admin"]))])
def critical(message: str):
    AlertEngine.critical_error(message)
    return {"message": "Critical alert sent"}
