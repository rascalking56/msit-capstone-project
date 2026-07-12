from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from my_app.database import Base, engine

# Import all route modules
from my_app.routes import (
    auth_routes,
    product_routes,
    order_routes,
    inventory_routes,
    alert_routes,
    user_routes,
    audit_routes,   # ← NEW
)

# -----------------------------
# Initialize FastAPI App
# -----------------------------
app = FastAPI(
    title="Order Management System",
    description="Backend API for Orders, Inventory, Alerts, Audit Logs, and Authentication",
    version="1.0.0",
)

# -----------------------------
# CORS (Frontend Compatibility)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Static Files (Frontend)
# -----------------------------
app.mount("/frontend", StaticFiles(directory="my_app/frontend"), name="frontend")

# -----------------------------
# Database Initialization
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(order_routes.router)
app.include_router(inventory_routes.router)
app.include_router(alert_routes.router)
app.include_router(user_routes.router)
app.include_router(audit_routes.router)   # ← THIS FIXES YOUR 404

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Order Management System API is running"}
