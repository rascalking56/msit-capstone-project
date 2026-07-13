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


def test_create_order():
    response = client.post("/orders/", json={
        "customer_name": "John Doe",
        "item_name": "Laptop",
        "quantity": 1
    })
    assert response.status_code == 200
    assert response.json()["customer_name"] == "John Doe"


def test_update_order_status():
    client.post("/orders/", json={
        "customer_name": "Jane",
        "item_name": "Mouse",
        "quantity": 2
    })

    response = client.put("/orders/1", json={"status": "processing"})
    assert response.status_code == 200
    assert response.json()["status"] == "processing"
