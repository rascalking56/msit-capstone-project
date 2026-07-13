from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# Database File Location
# ---------------------------------------------------------
DATABASE_URL = "sqlite:///C:/Users/rasca/OneDrive/Desktop/order_system/orders.db"

# ---------------------------------------------------------
# Engine
# ---------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# ---------------------------------------------------------
# Session
# ---------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------------------------
# Base Model Class
# ---------------------------------------------------------
Base = declarative_base()


# ---------------------------------------------------------
# Dependency: Get DB Session
# ---------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
