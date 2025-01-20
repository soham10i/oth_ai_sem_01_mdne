import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.main import app
from unittest.mock import patch, MagicMock
from app.database.connection import get_db
from app.models.user import UserCreate
from app.services.auth_service import create_user

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

def test_register_user():
    user_data = {
        "username": "newuser",
        "firstname": "New",
        "lastname": "User",
        "dob": "1995-01-01",
        "email": "newuser@example.com",
        "password": "password",
        "user_type": "resident"
    }
    try:
        response = client.post("/register", json=user_data)
        assert response.status_code == 200
        assert response.json()["email"] == "newuser@example.com"
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_register_existing_user(test_user):
    user_data = {
        "username": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "dob": "1990-01-01",
        "email": "testuser@example.com",
        "password": "password",
        "user_type": "resident"
    }
    try:
        response = client.post("/register", json=user_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_login_user(test_user):
    login_data = {
        "email": "admin.one@mail.com",
        "password": "AdminOne@123456"
    }
    try:
        response = client.post("/login", json=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_login_invalid_user():
    login_data = {
        "email": "invaliduser@example.com",
        "password": "password"
    }
    try:
        response = client.post("/login", json=login_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid email or password"
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_login_invalid_password(test_user):
    login_data = {
        "email": "testuser@example.com",
        "password": "wrongpassword"
    }
    try:
        response = client.post("/login", json=login_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid email or password"
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_get_user_details(test_user):
    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email

def test_update_user_details(test_user):
    update_data = {
        "firstname": "Updated",
        "lastname": "User",
        "dob": "1990-01-01",
        "email": "updateduser@example.com",
        "password": "newpassword",
        "user_type": "resident"
    }
    response = client.put(f"/users/{test_user.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["email"] == "updateduser@example.com"

def test_delete_user(test_user):
    response = client.delete(f"/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted successfully"
