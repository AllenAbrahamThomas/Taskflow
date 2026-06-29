import pytest
from app.models.user import User

def test_task_lifecycle(client, admin_headers, dev_headers, db):
    # 1. Create a project first
    project = client.post(
        "/api/v1/projects/",
        json={"name": "Task Test Project", "description": "Testing tasks"},
        headers=admin_headers
    )
    assert project.status_code == 201
    project_id = project.json()["id"]

    # Get developer user id
    dev_user = db.query(User).filter(User.email == "testdev@example.com").first()
    dev_id = str(dev_user.id)

    # 2. Create task (Admin only)
    task_response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Build DB Models",
            "description": "Create users, projects and tasks tables",
            "project_id": project_id,
            "status": "todo"
        },
        headers=admin_headers
    )
    assert task_response.status_code == 201
    task_id = task_response.json()["id"]
    assert task_response.json()["title"] == "Build DB Models"
    assert task_response.json()["status"] == "todo"

    # 3. Try status update by Developer when unassigned (should fail 403)
    status_fail = client.put(
        f"/api/v1/tasks/{task_id}/status",
        json={"status": "in_progress"},
        headers=dev_headers
    )
    assert status_fail.status_code == 403

    # 4. Assign task to Developer (Admin only)
    assign_response = client.put(
        f"/api/v1/tasks/{task_id}/assign",
        json={"assigned_to": dev_id},
        headers=admin_headers
    )
    assert assign_response.status_code == 200
    assert assign_response.json()["assigned_to"] == dev_id

    # 5. Developer updates status of assigned task (should succeed)
    status_success = client.put(
        f"/api/v1/tasks/{task_id}/status",
        json={"status": "in_progress"},
        headers=dev_headers
    )
    assert status_success.status_code == 200
    assert status_success.json()["status"] == "in_progress"

    # 6. List tasks with filtering
    # Filter by project
    list_resp = client.get(f"/api/v1/tasks/?project_id={project_id}", headers=dev_headers)
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == task_id

    # Filter by status
    list_resp_status = client.get(f"/api/v1/tasks/?status=in_progress", headers=dev_headers)
    assert list_resp_status.json()["total"] == 1

    list_resp_todo = client.get(f"/api/v1/tasks/?status=todo", headers=dev_headers)
    assert list_resp_todo.json()["total"] == 0

    # Filter by assigned_to
    list_resp_assigned = client.get(f"/api/v1/tasks/?assigned_to={dev_id}", headers=dev_headers)
    assert list_resp_assigned.json()["total"] == 1
