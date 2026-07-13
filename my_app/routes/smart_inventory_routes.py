from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.auth.auth_handler import require_role
from my_app.services.smart_inventory_service import SmartInventoryService

router = APIRouter(prefix="/inventory/smart", tags=["Smart Inventory"])


@router.get("/low-stock", dependencies=[Depends(require_role(["admin", "staff"]))])
def low_stock(db: Session = Depends(get_db)):
    return SmartInventoryService.low_stock_alerts(db)


@router.get("/predict/{product_id}", dependencies=[Depends(require_role(["admin", "staff"]))])
def predict(product_id: int, db: Session = Depends(get_db)):
    return SmartInventoryService.predict_depletion(db, product_id)


@router.post("/auto-restock", dependencies=[Depends(require_role(["admin"]))])
def auto_restock(db: Session = Depends(get_db)):
    return SmartInventoryService.auto_restock(db)


@router.get("/trends", dependencies=[Depends(require_role(["admin", "staff"]))])
def trends(db: Session = Depends(get_db)):
    return SmartInventoryService.inventory_trends(db)
