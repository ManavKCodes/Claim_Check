from dataclasses import dataclass
from enum import StrEnum
from decimal import Decimal


class ComparatorStatus(StrEnum):
    MATCHED = "MATCHED"
    NO_VALID_COMPARATOR = "NO_VALID_COMPARATOR"
    AMBIGUOUS_COMPARATOR = "AMBIGUOUS_COMPARATOR"


@dataclass(frozen=True)
class ProductCandidate:
    product_id: str
    category: str | None
    product_family: str | None
    brand: str | None
    basis: str | None
    nutrient: str
    value: Decimal | None
    unit: str | None


@dataclass(frozen=True)
class ComparatorResolution:
    status: ComparatorStatus
    reference_product: ProductCandidate | None
    candidate_count: int
    matching_factors: dict[str, str]
    notes: str


def resolve_comparator(
    subject: ProductCandidate, candidates: list[ProductCandidate]
) -> ComparatorResolution:
    valid: list[tuple[ProductCandidate, dict[str, str]]] = []
    for candidate in candidates:
        factors = _matching_factors(subject, candidate)
        if factors is not None:
            valid.append((candidate, factors))

    if len(valid) == 1:
        candidate, factors = valid[0]
        return ComparatorResolution(
            status=ComparatorStatus.MATCHED,
            reference_product=candidate,
            candidate_count=1,
            matching_factors=factors,
            notes="Exactly one candidate passed category, family, basis, nutrient, and value checks.",
        )
    if not valid:
        return ComparatorResolution(
            status=ComparatorStatus.NO_VALID_COMPARATOR,
            reference_product=None,
            candidate_count=0,
            matching_factors={},
            notes="No candidate passed all compatibility checks.",
        )
    return ComparatorResolution(
        status=ComparatorStatus.AMBIGUOUS_COMPARATOR,
        reference_product=None,
        candidate_count=len(valid),
        matching_factors={},
        notes="Multiple candidates passed; no candidate was selected implicitly.",
    )


def _matching_factors(subject: ProductCandidate, candidate: ProductCandidate) -> dict[str, str] | None:
    if subject.product_id == candidate.product_id:
        return None
    if not _same_text(subject.category, candidate.category):
        return None
    if not _same_text(subject.basis, candidate.basis):
        return None
    if subject.nutrient.casefold() != candidate.nutrient.casefold():
        return None
    if subject.unit != candidate.unit or candidate.value is None:
        return None
    if subject.product_family and not _same_text(subject.product_family, candidate.product_family):
        return None
    factors = {"category": "exact", "basis": "exact", "nutrient": "exact", "unit": "exact"}
    if subject.product_family:
        factors["product_family"] = "exact"
    if subject.brand and candidate.brand and _same_text(subject.brand, candidate.brand):
        factors["brand"] = "exact"
    return factors


def _same_text(left: str | None, right: str | None) -> bool:
    return bool(left and right and left.strip().casefold() == right.strip().casefold())
