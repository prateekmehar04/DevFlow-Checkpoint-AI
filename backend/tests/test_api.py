from fastapi.testclient import TestClient

from app.main import app
from app.storage import store


def setup_function():
    store.reset()


client = TestClient(app)


def test_project_checkpoint_diff_and_restore_flow():
    project_response = client.post(
        "/api/v1/projects",
        json={"name": "Hackathon Demo", "description": "Stateful Bob workflow"},
    )
    assert project_response.status_code == 201
    project = project_response.json()

    first = client.post(
        "/api/v1/checkpoints",
        json={
            "project_id": project["id"],
            "milestone": "plan",
            "state_data": {"files": ["README.md"], "status": "planned"},
            "metadata": {"author": "tester"},
        },
    ).json()
    second = client.post(
        "/api/v1/checkpoints",
        json={
            "project_id": project["id"],
            "milestone": "code",
            "state_data": {"files": ["README.md", "app.py"], "status": "coded"},
            "metadata": {"author": "tester"},
        },
    ).json()

    diff_response = client.get(f"/api/v1/checkpoints/diff?left_id={first['id']}&right_id={second['id']}")
    assert diff_response.status_code == 200
    diff = diff_response.json()["diff"]
    assert diff["added"]
    assert diff["changed"]

    restore_response = client.post(f"/api/v1/checkpoints/{first['id']}/restore")
    assert restore_response.status_code == 200
    assert restore_response.json()["state_data"]["status"] == "planned"


def test_workflow_transition_creates_checkpoint_and_blocks_invalid_jump():
    project = client.post("/api/v1/projects", json={"name": "Workflow Demo"}).json()
    workflow_response = client.post(
        "/api/v1/workflows",
        json={"project_id": project["id"], "context": {"goal": "demo"}},
    )
    assert workflow_response.status_code == 201
    workflow = workflow_response.json()

    transition_response = client.post(
        f"/api/v1/workflows/{workflow['id']}/transition",
        json={"target_state": "code", "note": "plan approved"},
    )
    assert transition_response.status_code == 200
    transitioned = transition_response.json()
    assert transitioned["current_state"] == "code"
    assert transitioned["last_checkpoint_id"]

    invalid_response = client.post(
        f"/api/v1/workflows/{workflow['id']}/transition",
        json={"target_state": "done"},
    )
    assert invalid_response.status_code == 409


def test_bob_local_demo_endpoints():
    plan_response = client.post(
        "/api/v1/bob/plan",
        json={"project_description": "Build checkpoint AI for Bob", "context": {"focus": "hackathon"}},
    )
    assert plan_response.status_code == 200
    assert plan_response.json()["agent"] == "planning"

    test_response = client.post(
        "/api/v1/bob/test",
        json={"code": "def add(a, b): return a + b", "test_type": "unit", "context": {}},
    )
    assert test_response.status_code == 200
    assert test_response.json()["recommended_cases"]
