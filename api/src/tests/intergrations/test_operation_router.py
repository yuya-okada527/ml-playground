from fastapi.testclient import TestClient
from main import app

HEALTH_CHECK_API_PATH = "/"

client = TestClient(app)


def test_ping():
    response = client.get(HEALTH_CHECK_API_PATH)
    assert response.status_code == 200
