from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_rules_endpoint_returns_versioned_catalog() -> None:
    response = TestClient(app).get("/api/rules")

    assert response.status_code == 200
    assert len(response.json()) == 5
    assert all(rule["status"] == "PENDING_SOURCE_VERIFICATION" for rule in response.json())


def test_database_health_reports_configured_backend() -> None:
    response = TestClient(app).get("/health/database")

    assert response.status_code == 200
    assert response.json()["status"] == "configured"
