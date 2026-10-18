"""
Tests for the CommitmentSync main application.
"""
from fastapi.testclient import TestClient
from src.commitmentsync.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health endpoint returns correct response."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


def test_optimize_endpoint_high_utilization():
    """Test optimization endpoint with high utilization."""
    response = client.post(
        "/optimize",
        json={
            "cluster_id": "test-cluster-1",
            "cpu_utilization": 0.8,
            "memory_utilization": 0.9,
            "storage_utilization": 0.7,
            "hourly_cost": 10.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cluster_id"] == "test-cluster-1"
    assert data["recommended_reservation_type"] == "Standard Reserved Instance"
    assert data["recommended_term_months"] == 12
    assert data["estimated_savings_percent"] == 30.0
    assert data["confidence_score"] == 0.8


def test_optimize_endpoint_low_utilization():
    """Test optimization endpoint with low utilization."""
    response = client.post(
        "/optimize",
        json={
            "cluster_id": "test-cluster-2",
            "cpu_utilization": 0.2,
            "memory_utilization": 0.3,
            "storage_utilization": 0.1,
            "hourly_cost": 5.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cluster_id"] == "test-cluster-2"
    assert data["recommended_reservation_type"] == "On-Demand (no reservation)"
    assert data["recommended_term_months"] == 0
    assert data["estimated_savings_percent"] == 0.0
    assert data["confidence_score"] == 0.9