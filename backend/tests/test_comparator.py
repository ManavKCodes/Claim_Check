from decimal import Decimal

from app.comparator.resolver import ComparatorStatus, ProductCandidate, resolve_comparator


def product(product_id: str, **overrides: object) -> ProductCandidate:
    values: dict[str, object] = {
        "product_id": product_id,
        "category": "cereal",
        "product_family": "breakfast cereal",
        "brand": "Example",
        "basis": "per_100g",
        "nutrient": "protein",
        "value": Decimal("10"),
        "unit": "g",
    }
    values.update(overrides)
    return ProductCandidate(**values)


def test_matching_comparator_is_returned() -> None:
    result = resolve_comparator(product("subject"), [product("reference")])

    assert result.status == ComparatorStatus.MATCHED
    assert result.reference_product is not None
    assert result.reference_product.product_id == "reference"
    assert result.candidate_count == 1


def test_no_valid_comparator_for_incompatible_basis_or_missing_value() -> None:
    result = resolve_comparator(
        product("subject"),
        [product("wrong-basis", basis="per_serving"), product("missing-value", value=None)],
    )

    assert result.status == ComparatorStatus.NO_VALID_COMPARATOR
    assert result.reference_product is None


def test_multiple_valid_comparators_are_ambiguous() -> None:
    result = resolve_comparator(product("subject"), [product("reference-1"), product("reference-2")])

    assert result.status == ComparatorStatus.AMBIGUOUS_COMPARATOR
    assert result.reference_product is None
    assert result.candidate_count == 2


def test_same_product_is_never_its_own_comparator() -> None:
    result = resolve_comparator(product("subject"), [product("subject")])

    assert result.status == ComparatorStatus.NO_VALID_COMPARATOR


def test_family_mismatch_is_rejected_even_when_category_matches() -> None:
    result = resolve_comparator(product("subject"), [product("reference", product_family="granola")])

    assert result.status == ComparatorStatus.NO_VALID_COMPARATOR
