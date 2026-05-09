import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Generate a unique email for each test run to avoid database conflicts
unique_email = f"testuser_{int(time.time())}@example.com"
test_password = "securepassword123"


def test_register_user():
    # Test successful user registration
    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Test Employee",
            "role": "employee",
            "password": test_password
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == unique_email
    assert "id" in data

    # Ensure backend forces all new users to Employee role
    assert data["role"] == "employee"


def test_register_existing_user():
    # Test registering an email that already exists
    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "full_name": "Test Employee 2",
            "role": "employee",
            "password": test_password
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_admin_attempt_forced_to_employee():
    # Test that admin role registration is blocked
    response = client.post(
        "/auth/register",
        json={
            "email": f"admin_attempt_{int(time.time())}@example.com",
            "full_name": "Fake Admin",
            "role": "admin",
            "password": test_password
        }
    )

    assert response.status_code == 200

    data = response.json()

    # Backend should force employee role
    assert data["role"] == "employee"


def test_login_success():
    # Test successful login with correct credentials
    response = client.post(
        "/auth/login",
        data={"username": unique_email, "password": test_password}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    # Test login with incorrect password
    response = client.post(
        "/auth/login",
        data={"username": unique_email, "password": "wrongpassword"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"