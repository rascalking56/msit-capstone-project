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


def test_restock_inventory():
    client.post("/products/", json={
        "name": "Keyboard",
        "description": "Mechanical",
        "price": 99.99,
        "stock": 5
    })

    response = client.post("/inventory/restock/1?amount=10")
    assert response.status_code == 200
    assert response.json()["new_stock"] == 15


def test_reduce_inventory():
    client.post("/products/", json={
        "name": "Monitor",
        "description": "4K",
        "price": 300.00,
        "stock": 20
    })

    response = client.post("/inventory/reduce/1?amount=5")
    assert response.status_code == 200
    assert response.json()["new_stock"] == 15
