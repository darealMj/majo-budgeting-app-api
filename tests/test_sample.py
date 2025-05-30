import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Sample test - API root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "MAJO Budgeting App" in data["message"]


def test_health_endpoint(client: TestClient) -> None:
    """Sample test - Health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.slow
def test_api_documentation_accessible(client: TestClient) -> None:
    """Sample test - API docs accessibility"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_api_v1_root(client: TestClient) -> None:
    """Test API v1 root endpoint."""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "MAJO Budgeting App API v1"


@pytest.mark.unit
def test_basic_math() -> None:
    """Sample unit test."""
    assert 2 + 2 == 4
    assert 10 / 2 == 5.0
