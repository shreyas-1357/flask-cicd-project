import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_home_returns_json(client):
    response = client.get('/')
    data = response.get_json()
    assert "message" in data
    assert "status" in data

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_version_endpoint(client):
    response = client.get('/version')
    assert response.status_code == 200
    assert "version" in response.get_json()