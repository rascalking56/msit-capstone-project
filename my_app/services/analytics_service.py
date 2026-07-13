from sqlalchemy.orm import Session
from sqlalchemy import func
from my_app.models.order import Order
from my_app.models.product import Product


class AnalyticsService:

    # ---------------------------------------------------------
    # SALES ANALYTICS
    # ---------------------------------------------------------

    @staticmethod
    def sales_daily(db: Session):
        return (
            db.query(
                func.date(Order.created_at).label("day"),
                func.sum(Order.quantity).label("total")
            )
            .group_by(func.date(Order.created_at))
            .order_by(func.date(Order.created_at))
            .all()
        )

    @staticmethod
    def sales_weekly(db: Session):
        return (
            db.query(
                func.date_trunc("week", Order.created_at).label("week"),
                func.sum(Order.quantity).label("total")
            )
            .group_by(func.date_trunc("week", Order.created_at))
            .order_by(func.date_trunc("week", Order.created_at))
            .all()
        )

    @staticmethod
    def sales_monthly(db: Session):
        return (
            db.query(
                func.date_trunc("month", Order.created_at).label("month"),
                func.sum(Order.quantity).label("total")
            )
            .group_by(func.date_trunc("month", Order.created_at))
            .order_by(func.date_trunc("month", Order.created_at))
            .all()
        )

    # ---------------------------------------------------------
    # REVENUE ANALYTICS
    # ---------------------------------------------------------

    @staticmethod
    def revenue_trends(db: Session):
        return (
            db.query(
                func.date(Order.created_at).label("day"),
                func.sum(Order.quantity * Product.price).label("revenue")
            )
            .join(Product, Product.id == Order.product_id)
            .group_by(func.date(Order.created_at))
            .order_by(func.date(Order.created_at))
            .all()
        )

    # ---------------------------------------------------------
    # TOP SELLING PRODUCTS
    # ---------------------------------------------------------

    @staticmethod
    def top_selling_products(db: Session, limit: int = 10):
        return (
            db.query(
                Product.name.label("product"),
                func.sum(Order.quantity).label("total_sold")
            )
            .join(Product, Product.id == Order.product_id)
            .group_by(Product.name)
            .order_by(func.sum(Order.quantity).desc())
            .limit(limit)
            .all()
        )

    # ---------------------------------------------------------
    # CUSTOMER PURCHASE PATTERNS
    # ---------------------------------------------------------

    @staticmethod
    def customer_purchase_patterns(db: Session):
        return (
            db.query(
                Order.customer_username.label("customer"),
                func.count(Order.id).label("orders"),
                func.sum(Order.quantity).label("total_items"),
                func.sum(Order.quantity * Product.price).label("total_spent")
            )
            .join(Product, Product.id == Order.product_id)
            .group_by(Order.customer_username)
            .order_by(func.sum(Order.quantity * Product.price).desc())
            .all()
        )

    # ---------------------------------------------------------
    # INVENTORY TRENDS (Sales over time per product)
    # ---------------------------------------------------------

    @staticmethod
    def inventory_trends(db: Session):
        products = db.query(Product).all()
        trends = {}

        for p in products:
            sales = (
                db.query(
                    func.date(Order.created_at).label("day"),
                    func.sum(Order.quantity).label("sold")
                )
                .filter(Order.product_id == p.id)
                .group_by(func.date(Order.created_at))
                .order_by(func.date(Order.created_at))
                .all()
            )

            trends[p.name] = [
                {"day": s.day, "sold": s.sold}
                for s in sales
            ]

        return trends

    # ---------------------------------------------------------
    # SALES HEATMAP (Hour-of-day activity)
    # ---------------------------------------------------------

    @staticmethod
    def sales_heatmap(db: Session):
        return (
            db.query(
                func.extract("hour", Order.created_at).label("hour"),
                func.sum(Order.quantity).label("total")
            )
            .group_by(func.extract("hour", Order.created_at))
            .order_by(func.extract("hour", Order.created_at))
            .all()
        )

    # ---------------------------------------------------------
    # SALES BY PRODUCT (Daily)
    # ---------------------------------------------------------

    @staticmethod
    def sales_by_product_daily(db: Session):
        return (
            db.query(
                Product.name.label("product"),
                func.date(Order.created_at).label("day"),
                func.sum(Order.quantity).label("total")
            )
            .join(Product, Product.id == Order.product_id)
            .group_by(Product.name, func.date(Order.created_at))
            .order_by(Product.name, func.date(Order.created_at))
            .all()
        )
