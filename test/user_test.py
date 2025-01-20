import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database.connection import get_db
from app.models.user import User, UserCreate
from app.services.auth_service import create_user, create_access_token

client = TestClient(app)

def override_get_db():
    # Provide a test database session
    yield Session()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def test_user(db: Session):
    user_data = UserCreate(
        username="testuser",
        firstname="Test",
        lastname="User",
        dob="1990-01-01",
        email="testuser@example.com",
        password="password",
        user_type="resident"
    )
    user = create_user(db, user_data)
    return user

@pytest.fixture
def admin_user(db: Session):
    user_data = UserCreate(
        username="adminuser",
        firstname="Admin",
        lastname="User",
        dob="1980-01-01",
        email="adminuser@example.com",
        password="password",
        user_type="admin"
    )
    user = create_user(db, user_data)
    return user

@pytest.fixture
def auth_headers(test_user: User):
    access_token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def admin_auth_headers(admin_user: User):
    access_token = create_access_token(data={"sub": admin_user.email})
    return {"Authorization": f"Bearer {access_token}"}

def test_get_current_user_details(auth_headers):
    try:
        response = client.get("/profile", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "testuser@example.com"
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_update_current_user(auth_headers):
    update_data = {
        "username": "updateduser",
        "firstname": "Updated",
        "lastname": "User",
        "dob": "1990-01-01",
        "email": "updateduser@example.com",
        "password": "newpassword",
        "user_type": "resident"
    }
    try:
        response = client.put("/update", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["username"] == "updateduser"
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_delete_current_user(admin_auth_headers):
    try:
        response = client.delete("/delete", headers=admin_auth_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "adminuser@example.com"
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_fetch_all_users(admin_auth_headers):
    try:
        response = client.get("/all", headers=admin_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
