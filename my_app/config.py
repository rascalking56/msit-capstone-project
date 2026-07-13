import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file if present
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


# -----------------------------
# Project Metadata
# -----------------------------
PROJECT_NAME = "Order & Inventory Management System"
VERSION = "1.0.0"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


# -----------------------------
# Database Configuration
# -----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./my_app.db"  # default fallback
)


# -----------------------------
# JWT Configuration
# -----------------------------
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)
)


# -----------------------------
# Refresh Token Configuration
# -----------------------------
REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30)
)


# -----------------------------
# Audit Logging Configuration
# -----------------------------
AUDIT_ENABLED = os.getenv("AUDIT_ENABLED", "true").lower() == "true"
AUDIT_MAX_RECORDS = int(os.getenv("AUDIT_MAX_RECORDS", 5000))


# -----------------------------
# Inventory Alerts Configuration
# -----------------------------
LOW_STOCK_THRESHOLD = int(os.getenv("LOW_STOCK_THRESHOLD", 5))
FAILED_LOGIN_ALERT_WINDOW_MIN = int(
    os.getenv("FAILED_LOGIN_ALERT_WINDOW_MIN", 30)
)


# -----------------------------
# Helper Functions
# -----------------------------
def is_production():
    return ENVIRONMENT.lower() == "production"


def is_development():
    return ENVIRONMENT.lower() == "development"


def print_config_summary():
    print("=== CONFIG SUMMARY ===")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Database URL: {DATABASE_URL}")
    print(f"JWT Algorithm: {JWT_ALGORITHM}")
    print(f"Access Token Expiration: {ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
    print(f"Refresh Token Expiration: {REFRESH_TOKEN_EXPIRE_DAYS} days")
    print(f"Audit Logging Enabled: {AUDIT_ENABLED}")
    print(f"Low Stock Threshold: {LOW_STOCK_THRESHOLD}")
    print("======================")
