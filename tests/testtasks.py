from tests.conftest import client


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "CI Test",
            "description": "Testing",
            "due_date": "2026-12-31",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "CI Test"

def test_list_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200

def test_get_task():
    response = client.get("/tasks/1")

    assert response.status_code == 200

def test_complete_task():
    response = client.patch("/tasks/1/complete")

    assert response.status_code == 200