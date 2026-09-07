from decimal import Decimal

from app.evidence.trail import EvidenceItem
from app.verification.service import verify_claim


def evidence(field_name: str, value: str | None, unit: str | None = None) -> EvidenceItem:
    return EvidenceItem.create(
        field_name=field_name,
        source_type="test",
        raw_value=value,
        normalized_value=value,
        unit=unit,
    )


def test_pending_rule_returns_insufficient_evidence() -> None:
    result = verify_claim(
        "HIGH_PROTEIN",
        "High Protein",
        [evidence("claim", "High Protein"), evidence("subject_protein", "20", "g")],
    )

    assert result.evaluation.verdict == "INSUFFICIENT_EVIDENCE"
    assert "verified_rule" in result.evaluation.missing_evidence
    assert result.rule is not None


def test_comparative_claim_without_matched_comparator_abstains() -> None:
    result = verify_claim(
        "COMPARATIVE_PROTEIN",
        "30% More Protein",
        [evidence("claim", "30% More Protein"), evidence("subject_protein", "26", "g")],
        comparator_status="NO_VALID_COMPARATOR",
    )

    assert result.evaluation.verdict == "INSUFFICIENT_EVIDENCE"
    assert result.evaluation.missing_evidence == ("valid_comparator",)


def test_verification_identifier_is_stable_for_identical_input() -> None:
    items = [evidence("claim", "Low Fat"), evidence("subject_fat", "5", "g")]
    first = verify_claim("LOW_FAT", "Low Fat", items)
    second = verify_claim("LOW_FAT", "Low Fat", items)

    assert first.verification_id == second.verification_id


def test_unknown_claim_type_abstains_without_rule() -> None:
    result = verify_claim("UNKNOWN", "Unrecognized claim", [])

    assert result.rule is None
    assert result.evaluation.verdict == "INSUFFICIENT_EVIDENCE"
    assert result.evaluation.rule_id == "NO_APPLICABLE_RULE"
