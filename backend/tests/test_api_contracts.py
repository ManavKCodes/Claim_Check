from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_claim_classification_exposes_ontology_metadata() -> None:
    response = client.post("/api/claim/classify", json={"raw_text": "High in protein"})

    assert response.status_code == 200
    assert response.json()["claim_type"] == "HIGH_PROTEIN"
    assert response.json()["requires_comparator"] is False


def test_product_analysis_preserves_raw_claim_and_source() -> None:
    response = client.post(
        "/api/product/analyze",
        json={"product_name": "Example", "product_source_reference": "source-1", "claim_text": "Low Fat"},
    )

    assert response.status_code == 200
    assert response.json()["claim"]["raw_claim"] == "Low Fat"
    assert response.json()["product_source_reference"] == "source-1"


def test_verification_response_contains_evidence_and_abstains_pending_rule() -> None:
    response = client.post(
        "/api/verify",
        json={
            "claim_type": "HIGH_PROTEIN",
            "raw_claim": "High Protein",
            "evidence": [
                {"field_name": "claim", "source_type": "test", "raw_value": "High Protein", "normalized_value": "High Protein"},
                {"field_name": "subject_protein", "source_type": "test", "raw_value": "20", "normalized_value": "20", "unit": "g"},
            ],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert body["rule_id"].startswith("FSSAI-")
    assert len(body["evidence"]) == 2


def test_evaluation_endpoint_reports_empty_benchmark_without_scores() -> None:
    response = client.post("/api/evaluation/run")

    assert response.status_code == 200
    assert response.json()["status"] == "NOT_YET_MEASURED"
    assert response.json()["sample_count"] == 0
