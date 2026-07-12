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


def test_create_product():
    response = client.post("/products/", json={
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1500.00,
        "stock": 10
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_update_product():
    client.post("/products/", json={
        "name": "Mouse",
        "description": "Wireless",
        "price": 25.00,
        "stock": 50
    })

    response = client.put("/products/1", json={"price": 30.00})
    assert response.status_code == 200
    assert response.json()["price"] == 30.00
