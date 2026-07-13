from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------
from my_app.database import Base, engine

# Import ALL models so SQLAlchemy can create tables
from my_app.models.user import User
from my_app.models.order import Order
from my_app.models.product import Product

# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
from my_app.routes.auth_routes import router as auth_router
from my_app.routes.user_routes import router as user_router
from my_app.routes.order_routes import router as order_router
from my_app.routes.product_routes import router as product_router
from my_app.routes.inventory_routes import router as inventory_router
from my_app.routes.alert_routes import router as alert_router
from my_app.routes.audit_routes import router as audit_router
from my_app.routes.analytics_routes import router as analytics_router


# ---------------------------------------------------------
# Create Database Tables
# ---------------------------------------------------------
print(">>> Initializing database schema...")
Base.metadata.create_all(bind=engine)
print(">>> Database ready.")


# ---------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------
app = FastAPI(title="Order Management System API")


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Include Routers
# ---------------------------------------------------------
app.include_router(auth_router)
app.include_router(user_router)        # <-- THIS FIXES /users/register
app.include_router(order_router)
app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(alert_router)
app.include_router(audit_router)
app.include_router(analytics_router)


# ---------------------------------------------------------
# Startup Event
# ---------------------------------------------------------
@app.on_event("startup")
def startup_event():
    print(">>> Application startup complete.")


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Order Management System API is running"}
