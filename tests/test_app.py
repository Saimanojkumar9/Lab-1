import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_list_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_prevent_duplicate():
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser@mergington.edu"
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    activities = client.get("/activities").json()
    participants = activities[activity]["participants"]
    assert participants.count(email) == 1

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=ghost@mergington.edu")
    assert response.status_code == 404

def test_unregister_participant():
    activity = next(iter(client.get("/activities").json().keys()))
    email = "removeuser@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

def test_unregister_nonexistent_participant():
    activity = next(iter(client.get("/activities").json().keys()))
    response = client.delete(f"/activities/{activity}/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
