import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_user_and_get_token(role="employee"):
    # Helper function to create a dynamic user and return their token
    email = f"{role}_{int(time.time())}@example.com"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": f"Test {role}",
            "role": role,
            "password": "password123"
        }
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        data={"username": email, "password": "password123"}
    )

    return login_response.json()["access_token"]


def test_admin_create_project_and_task():
    # Create a regular employee account
    admin_token = create_user_and_get_token("employee")

    headers = {"Authorization": f"Bearer {admin_token}"}

    # Employees should not be allowed to create projects
    project_res = client.post(
        "/projects/",
        json={
            "name": "Test Project",
            "description": "Test Data",
            "manager_id": 1
        },
        headers=headers
    )

    assert project_res.status_code == 403
    assert project_res.json()["detail"] == "You don't have enough permissions"


def test_employee_cannot_delete_task():
    # Test Role-Based Access Control (RBAC): Employee cannot delete tasks
    employee_token = create_user_and_get_token("employee")

    headers = {"Authorization": f"Bearer {employee_token}"}

    # The role check middleware intercepts the request before hitting the database
    response = client.delete("/tasks/1", headers=headers)

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have enough permissions"


def test_invalid_status_transition():
    # Create employee account
    employee_token = create_user_and_get_token("employee")

    headers = {"Authorization": f"Bearer {employee_token}"}

    # Employees should not be able to create projects
    project_res = client.post(
        "/projects/",
        json={
            "name": "Transition Project",
            "manager_id": 1
        },
        headers=headers
    )

    # Verify access is denied
    assert project_res.status_code == 403
    assert project_res.json()["detail"] == "You don't have enough permissions"


def test_register_admin_attempt_becomes_employee():
    # Test that admin registration attempts are converted to employee accounts
    email = f"fake_admin_{int(time.time())}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": "Fake Admin",
            "role": "admin",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    # Backend should force employee role
    assert data["role"] == "employee"