from dataclasses import replace
from decimal import Decimal

from app.rule_engine.evaluator import EvidenceValue, evaluate_rule
from app.rule_engine.rules.catalog import RULE_CATALOG, select_rule
from app.rule_engine.verdict import Verdict


def test_catalog_contains_one_pending_rule_per_claim() -> None:
    assert len(RULE_CATALOG) == 5
    assert all(rule.status == "PENDING_SOURCE_VERIFICATION" for rule in RULE_CATALOG)
    assert {rule.claim_type for rule in RULE_CATALOG} == {
        "HIGH_PROTEIN",
        "LOW_FAT",
        "NO_ADDED_SUGAR",
        "COMPARATIVE_PROTEIN",
        "REDUCED_SODIUM",
    }


def test_rule_selection_is_configuration_driven() -> None:
    rule = select_rule("HIGH_PROTEIN")

    assert rule is not None
    assert rule.claim_type == "HIGH_PROTEIN"
    assert select_rule("UNKNOWN") is None


def test_pending_rule_abstains_even_when_nutrition_exists() -> None:
    rule = select_rule("HIGH_PROTEIN")
    assert rule is not None
    result = evaluate_rule(
        rule,
        {
            "claim": "High Protein",
            "subject_protein": EvidenceValue(Decimal("20"), "g", "per_100g"),
            "applicable_rule": rule.rule_id,
        },
    )

    assert result.verdict == Verdict.INSUFFICIENT_EVIDENCE
    assert "verified_rule" in result.missing_evidence


def test_numeric_boundaries_are_deterministic_with_verified_test_rule() -> None:
    source_rule = select_rule("LOW_FAT")
    assert source_rule is not None
    rule = replace(source_rule, status="VERIFIED", threshold=Decimal("5"), threshold_type="less_than_or_equal", unit="g")

    at_boundary = evaluate_rule(
        rule,
        {"claim": "Low Fat", "subject_fat": EvidenceValue(Decimal("5"), "g", "per_100g"), "applicable_rule": rule.rule_id},
    )
    above_boundary = evaluate_rule(
        rule,
        {"claim": "Low Fat", "subject_fat": EvidenceValue(Decimal("5.1"), "g", "per_100g"), "applicable_rule": rule.rule_id},
    )

    assert at_boundary.verdict == Verdict.SUPPORTED
    assert above_boundary.verdict == Verdict.CONTRADICTED


def test_comparative_rule_rejects_zero_reference_and_calculates_percent() -> None:
    source_rule = select_rule("COMPARATIVE_PROTEIN")
    assert source_rule is not None
    rule = replace(source_rule, status="VERIFIED", threshold=Decimal("30"), threshold_type="percentage_at_least")
    supported = evaluate_rule(
        rule,
        {
            "claim": "30% More Protein",
            "subject_protein": EvidenceValue(Decimal("26"), "g", "per_100g"),
            "reference_product": "reference-1",
            "reference_protein": EvidenceValue(Decimal("20"), "g", "per_100g"),
            "comparable_basis": "per_100g",
            "applicable_rule": rule.rule_id,
        },
    )
    zero_reference = evaluate_rule(
        rule,
        {
            "claim": "30% More Protein",
            "subject_protein": EvidenceValue(Decimal("26"), "g", "per_100g"),
            "reference_product": "reference-1",
            "reference_protein": EvidenceValue(Decimal("0"), "g", "per_100g"),
            "comparable_basis": "per_100g",
            "applicable_rule": rule.rule_id,
        },
    )

    assert supported.verdict == Verdict.SUPPORTED
    assert supported.calculation is not None
    assert Decimal(supported.calculation["percentage"]) == Decimal("30")
    assert zero_reference.verdict == Verdict.INSUFFICIENT_EVIDENCE


def test_wrong_unit_abstains() -> None:
    source_rule = select_rule("HIGH_PROTEIN")
    assert source_rule is not None
    rule = replace(source_rule, status="VERIFIED", threshold=Decimal("10"), threshold_type="greater_than_or_equal", unit="g")
    result = evaluate_rule(
        rule,
        {"claim": "High Protein", "subject_protein": EvidenceValue(Decimal("10"), "mg", "per_100g"), "applicable_rule": rule.rule_id},
    )

    assert result.verdict == Verdict.INSUFFICIENT_EVIDENCE
