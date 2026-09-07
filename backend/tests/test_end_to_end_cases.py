from decimal import Decimal

from app.evidence.trail import EvidenceItem
from app.rule_engine.evaluator import EvidenceValue, evaluate_rule
from app.rule_engine.rules.catalog import select_rule
from app.rule_engine.verdict import Verdict
from app.verification.service import verify_claim


def test_case_supported_claim_with_verified_test_rule() -> None:
    rule = select_rule("HIGH_PROTEIN")
    assert rule is not None
    from dataclasses import replace

    verified_rule = replace(rule, status="VERIFIED", threshold=Decimal("10"), threshold_type="greater_than_or_equal", unit="g")
    result = evaluate_rule(verified_rule, {"claim": "High Protein", "subject_protein": EvidenceValue(Decimal("20"), "g", "per_100g"), "applicable_rule": verified_rule.rule_id})

    assert result.verdict == Verdict.SUPPORTED


def test_case_contradicted_claim_with_verified_test_rule() -> None:
    rule = select_rule("LOW_FAT")
    assert rule is not None
    from dataclasses import replace

    verified_rule = replace(rule, status="VERIFIED", threshold=Decimal("5"), threshold_type="less_than_or_equal", unit="g")
    result = evaluate_rule(verified_rule, {"claim": "Low Fat", "subject_fat": EvidenceValue(Decimal("8"), "g", "per_100g"), "applicable_rule": verified_rule.rule_id})

    assert result.verdict == Verdict.CONTRADICTED


def test_case_insufficient_comparative_claim_without_reference() -> None:
    result = verify_claim(
        "COMPARATIVE_PROTEIN",
        "30% More Protein",
        [EvidenceItem.create("claim", "test", raw_value="30% More Protein"), EvidenceItem.create("subject_protein", "test", raw_value="26", normalized_value="26", unit="g")],
        comparator_status="NO_VALID_COMPARATOR",
    )

    assert result.evaluation.verdict == Verdict.INSUFFICIENT_EVIDENCE
    assert "valid_comparator" in result.evaluation.missing_evidence
