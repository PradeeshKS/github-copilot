import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

def test_root_redirect(test_client: TestClient):
    """Test that root endpoint redirects to static/index.html"""
    response = test_client.get("/")
    assert response.status_code == 200  # Permanent redirect with RedirectResponse
    assert response.url.path == "/static/index.html"

def test_get_activities(test_client: TestClient):
    """Test fetching all activities"""
    response = test_client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    # Check some required fields in activities
    for activity in response.json().values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

def test_signup_for_activity(test_client: TestClient):
    """Test signing up for an activity"""
    activity_name = "Chess Club"
    email = "test@mergington.edu"
    
    # Try signing up
    response = test_client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify participant was added
    assert email in activities[activity_name]["participants"]

def test_signup_for_nonexistent_activity(test_client: TestClient):
    """Test signing up for an activity that doesn't exist"""
    response = test_client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_duplicate_signup(test_client: TestClient):
    """Test that a student cannot sign up for the same activity twice"""
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    
    # First signup should succeed
    response = test_client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    
    # Second signup should fail
    response = test_client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_unregister_from_activity(test_client: TestClient):
    """Test unregistering from an activity"""
    activity_name = "Chess Club"
    email = "unregister@mergington.edu"
    
    # First sign up
    test_client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Then unregister
    response = test_client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    
    # Verify participant was removed
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_registered(test_client: TestClient):
    """Test unregistering when not registered"""
    response = test_client.post("/activities/Chess Club/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"

def test_unregister_nonexistent_activity(test_client: TestClient):
    """Test unregistering from an activity that doesn't exist"""
    response = test_client.post("/activities/NonexistentClub/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"