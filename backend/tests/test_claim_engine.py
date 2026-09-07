import pytest

from app.claim_engine.extraction import extract_claim
from app.claim_engine.ontology.catalog import CLAIM_CATALOG


@pytest.mark.parametrize(
    ("raw_text", "claim_type"),
    [
        ("High in protein", "HIGH_PROTEIN"),
        ("LOW FAT", "LOW_FAT"),
        ("No sugar added", "NO_ADDED_SUGAR"),
        ("30% extra protein", "COMPARATIVE_PROTEIN"),
        ("Lower sodium", "REDUCED_SODIUM"),
    ],
)
def test_supported_aliases_normalize(raw_text: str, claim_type: str) -> None:
    result = extract_claim(raw_text, source="label_text")

    assert result.claim_type == claim_type
    assert result.normalized_claim == claim_type
    assert result.raw_claim == raw_text
    assert result.source == "label_text"
    assert result.confidence == 1.0


def test_unknown_claim_is_not_forced_into_ontology() -> None:
    result = extract_claim("Immune boosting goodness")

    assert result.claim_type is None
    assert result.normalized_claim is None
    assert result.confidence is None


def test_multiple_claims_are_ambiguous() -> None:
    result = extract_claim("High protein and low fat")

    assert result.claim_type is None
    assert result.normalized_claim is None


def test_catalog_contains_exactly_the_five_required_claims() -> None:
    assert {definition.claim_type for definition in CLAIM_CATALOG} == {
        "HIGH_PROTEIN",
        "LOW_FAT",
        "NO_ADDED_SUGAR",
        "COMPARATIVE_PROTEIN",
        "REDUCED_SODIUM",
    }
