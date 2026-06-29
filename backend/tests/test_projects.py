def test_create_project_admin(client, admin_headers):
    response = client.post(
        "/api/v1/projects/",
        json={"name": "Alpha Project", "description": "This is Alpha"},
        headers=admin_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alpha Project"
    assert "id" in data

def test_create_project_developer_denied(client, dev_headers):
    response = client.post(
        "/api/v1/projects/",
        json={"name": "Beta Project", "description": "This is Beta"},
        headers=dev_headers
    )
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

def test_list_projects(client, admin_headers, dev_headers):
    # Admin creates project
    client.post(
        "/api/v1/projects/",
        json={"name": "Project 1", "description": "Desc"},
        headers=admin_headers
    )
    
    # Dev lists projects
    response = client.get("/api/v1/projects/", headers=dev_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Project 1"

def test_update_project_admin(client, admin_headers):
    # Admin creates project
    proj_resp = client.post(
        "/api/v1/projects/",
        json={"name": "Project 2", "description": "Desc"},
        headers=admin_headers
    ).json()
    
    # Update project
    update_resp = client.put(
        f"/api/v1/projects/{proj_resp['id']}",
        json={"name": "Project 2 Updated"},
        headers=admin_headers
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Project 2 Updated"

def test_delete_project_admin(client, admin_headers):
    # Admin creates project
    proj_resp = client.post(
        "/api/v1/projects/",
        json={"name": "Project to Delete", "description": "Desc"},
        headers=admin_headers
    ).json()
    
    # Delete project
    del_resp = client.delete(
        f"/api/v1/projects/{proj_resp['id']}",
        headers=admin_headers
    )
    assert del_resp.status_code == 200
    
    # Verify 404
    get_resp = client.get(
        f"/api/v1/projects/{proj_resp['id']}",
        headers=admin_headers
    )
    assert get_resp.status_code == 404
