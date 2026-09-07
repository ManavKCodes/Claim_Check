from app.evidence.trail import EvidenceItem, build_evidence_trail, calculate_completeness


def test_complete_evidence_has_full_completeness() -> None:
    evidence = [
        EvidenceItem.create("claim", "packaging_image", raw_value="High Protein"),
        EvidenceItem.create("subject_protein", "open_food_facts", normalized_value="20", unit="g"),
    ]

    result = calculate_completeness(["claim", "subject_protein"], evidence)

    assert result.score == 1.0
    assert result.missing_fields == ()


def test_empty_value_is_missing_and_never_zero() -> None:
    evidence = [EvidenceItem.create("subject_protein", "nutrition_table", raw_value=None, normalized_value=None)]

    result = calculate_completeness(["claim", "subject_protein"], evidence)

    assert result.score == 0.0
    assert result.missing_fields == ("claim", "subject_protein")


def test_duplicate_required_fields_are_deduplicated() -> None:
    evidence = [EvidenceItem.create("claim", "user_correction", normalized_value="Low Fat")]

    result = calculate_completeness(["claim", "claim"], evidence)

    assert result.required_fields == ("claim",)
    assert result.present_fields == ("claim",)
    assert result.score == 1.0


def test_evidence_trail_preserves_rule_comparator_calculation_and_verdict() -> None:
    evidence = (EvidenceItem.create("claim", "packaging_image", raw_value="30% More Protein"),)

    trail = build_evidence_trail(
        ["claim", "subject_protein", "reference_product"],
        evidence,
        rule_id="rule-1",
        rule_version="version-1",
        comparator={"status": "MATCHED"},
        calculation={"percentage": "30"},
        verdict="SUPPORTED",
    )

    assert trail.rule_id == "rule-1"
    assert trail.comparator == {"status": "MATCHED"}
    assert trail.calculation == {"percentage": "30"}
    assert trail.verdict == "SUPPORTED"
    assert trail.completeness.missing_fields == ("subject_protein", "reference_product")
