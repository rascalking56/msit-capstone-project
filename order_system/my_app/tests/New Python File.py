from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_app.database import Base, get_db
from my_app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = lambda: TestingSessionLocal()
client = TestClient(app)


def test_audit_logging():
    client.post("/products/", json={
        "name": "Tablet",
        "description": "Android",
        "price": 200.00,
        "stock": 10
    })

    client.put("/products/1", json={"price": 250.00})

    logs = client.get("/audit/dashboard")
    assert logs.status_code == 200
    assert len(logs.json()) > 0
