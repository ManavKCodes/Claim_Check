import pytest

from app.evaluation.baselines import MultimodalBaseline, ocr_keyword_baseline
from app.evaluation.metrics import evaluate_verdicts


def test_empty_metrics_are_not_fabricated() -> None:
    result = evaluate_verdicts([], [])

    assert result.sample_count == 0
    assert result.accuracy is None
    assert result.false_approval_rate is None


def test_metrics_report_false_approval_separately() -> None:
    result = evaluate_verdicts(["CONTRADICTED", "SUPPORTED", "INSUFFICIENT_EVIDENCE"], ["SUPPORTED", "SUPPORTED", "INSUFFICIENT_EVIDENCE"])

    assert result.false_approval_rate == 0.5
    assert result.abstention_coverage == pytest.approx(1 / 3)


def test_keyword_baseline_abstains_without_thresholds() -> None:
    result = ocr_keyword_baseline("High Protein")

    assert result.claim_type == "HIGH_PROTEIN"
    assert result.verdict.value == "INSUFFICIENT_EVIDENCE"


def test_multimodal_baseline_requires_external_configuration() -> None:
    with pytest.raises(NotImplementedError):
        MultimodalBaseline().predict("product-image-reference")
