import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def sample_activity_data():
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        }
    }