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


def test_login_and_refresh():
    client.post("/users/register", json={
        "username": "jon",
        "password": "secret",
        "role": "admin"
    })

    login = client.post("/auth/login", json={
        "username": "jon",
        "password": "secret"
    })

    assert login.status_code == 200
    refresh_token = login.json()["refresh_token"]

    refreshed = client.post("/auth/refresh", params={"refresh_token": refresh_token})
    assert refreshed.status_code == 200
    assert "access_token" in refreshed.json()
