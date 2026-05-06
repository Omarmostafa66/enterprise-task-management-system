import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_user_and_get_token(role="employee"):
    # Helper function to create a dynamic user and return their token
    email = f"{role}_{int(time.time())}@example.com"
    client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": f"Test {role}",
            "role": role,
            "password": "password123"
        }
    )
    login_response = client.post(
        "/auth/login",
        data={"username": email, "password": "password123"}
    )
    return login_response.json()["access_token"]


def test_admin_create_project_and_task():
    # Test creating a project and a task using an admin token
    admin_token = create_user_and_get_token("admin")
    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Create a project
    project_res = client.post(
        "/projects/",
        json={"name": "Test Project", "description": "Test Data", "manager_id": 1},
        headers=headers
    )
    assert project_res.status_code == 200
    project_id = project_res.json()["id"]

    # 2. Create a task linked to the project
    task_res = client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "project_id": project_id,
            "priority": "Medium",
            "status": "To Do"
        },
        headers=headers
    )
    assert task_res.status_code == 200
    assert task_res.json()["title"] == "Test Task"


def test_employee_cannot_delete_task():
    # Test Role-Based Access Control (RBAC): Employee cannot delete tasks
    employee_token = create_user_and_get_token("employee")
    headers = {"Authorization": f"Bearer {employee_token}"}

    # The role check middleware intercepts the request before hitting the database
    response = client.delete("/tasks/1", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have enough permissions"


def test_invalid_status_transition():
    # Test Business Logic: Prevent invalid task status changes (e.g., Done -> To Do)
    admin_token = create_user_and_get_token("admin")
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Create a project and a completed task
    project_res = client.post(
        "/projects/",
        json={"name": "Transition Project", "manager_id": 1},
        headers=headers
    )
    project_id = project_res.json()["id"]

    task_res = client.post(
        "/tasks/",
        json={"title": "Completed Task", "project_id": project_id, "status": "Done"},
        headers=headers
    )
    task_id = task_res.json()["id"]

    # Attempt to transition from Done to To Do
    update_res = client.put(
        f"/tasks/{task_id}",
        json={"status": "To Do"},
        headers=headers
    )
    assert update_res.status_code == 400
    assert "Invalid status transition" in update_res.json()["detail"]