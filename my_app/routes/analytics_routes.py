from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.auth.auth_handler import require_role
from my_app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# ---------------------------------------------------------
# SALES ANALYTICS
# ---------------------------------------------------------

@router.get("/sales/daily", dependencies=[Depends(require_role(["admin", "staff"]))])
def sales_daily(db: Session = Depends(get_db)):
    return AnalyticsService.sales_daily(db)


@router.get("/sales/weekly", dependencies=[Depends(require_role(["admin", "staff"]))])
def sales_weekly(db: Session = Depends(get_db)):
    return AnalyticsService.sales_weekly(db)


@router.get("/sales/monthly", dependencies=[Depends(require_role(["admin", "staff"]))])
def sales_monthly(db: Session = Depends(get_db)):
    return AnalyticsService.sales_monthly(db)


# ---------------------------------------------------------
# REVENUE ANALYTICS
# ---------------------------------------------------------

@router.get("/revenue", dependencies=[Depends(require_role(["admin", "staff"]))])
def revenue_trends(db: Session = Depends(get_db)):
    return AnalyticsService.revenue_trends(db)


# ---------------------------------------------------------
# TOP SELLING PRODUCTS
# ---------------------------------------------------------

@router.get("/top-products", dependencies=[Depends(require_role(["admin", "staff"]))])
def top_products(db: Session = Depends(get_db)):
    return AnalyticsService.top_selling_products(db)


# ---------------------------------------------------------
# CUSTOMER PURCHASE PATTERNS
# ---------------------------------------------------------

@router.get("/customers/patterns", dependencies=[Depends(require_role(["admin", "staff"]))])
def customer_patterns(db: Session = Depends(get_db)):
    return AnalyticsService.customer_purchase_patterns(db)


# ---------------------------------------------------------
# INVENTORY TRENDS
# ---------------------------------------------------------

@router.get("/inventory/trends", dependencies=[Depends(require_role(["admin", "staff"]))])
def inventory_trends(db: Session = Depends(get_db)):
    return AnalyticsService.inventory_trends(db)


# ---------------------------------------------------------
# SALES HEATMAP (Hour-of-day activity)
# ---------------------------------------------------------

@router.get("/sales/heatmap", dependencies=[Depends(require_role(["admin", "staff"]))])
def sales_heatmap(db: Session = Depends(get_db)):
    return AnalyticsService.sales_heatmap(db)


# ---------------------------------------------------------
# SALES BY PRODUCT (Daily)
# ---------------------------------------------------------

@router.get("/sales/by-product/daily", dependencies=[Depends(require_role(["admin", "staff"]))])
def sales_by_product_daily(db: Session = Depends(get_db)):
    return AnalyticsService.sales_by_product_daily(db)
