from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class EvidenceItem:
    source_type: str
    source_reference: str | None
    image_reference: str | None
    field_name: str
    raw_value: str | None
    normalized_value: str | None
    unit: str | None
    extraction_method: str | None
    confidence: float | None
    created_at: datetime

    @classmethod
    def create(
        cls,
        field_name: str,
        source_type: str,
        raw_value: str | None = None,
        normalized_value: str | None = None,
        source_reference: str | None = None,
        image_reference: str | None = None,
        unit: str | None = None,
        extraction_method: str | None = None,
        confidence: float | None = None,
    ) -> "EvidenceItem":
        return cls(
            source_type=source_type,
            source_reference=source_reference,
            image_reference=image_reference,
            field_name=field_name,
            raw_value=raw_value,
            normalized_value=normalized_value,
            unit=unit,
            extraction_method=extraction_method,
            confidence=confidence,
            created_at=datetime.now(timezone.utc),
        )

    @property
    def has_value(self) -> bool:
        return bool(self.normalized_value or self.raw_value)


@dataclass(frozen=True)
class EvidenceCompleteness:
    required_fields: tuple[str, ...]
    present_fields: tuple[str, ...]
    missing_fields: tuple[str, ...]
    score: float


@dataclass(frozen=True)
class EvidenceTrail:
    evidence: tuple[EvidenceItem, ...]
    rule_id: str | None
    rule_version: str | None
    comparator: dict[str, Any] | None
    calculation: dict[str, Any] | None
    verdict: str | None
    completeness: EvidenceCompleteness


def calculate_completeness(
    required_fields: list[str] | tuple[str, ...], evidence: list[EvidenceItem] | tuple[EvidenceItem, ...]
) -> EvidenceCompleteness:
    required = tuple(dict.fromkeys(required_fields))
    present_names = {item.field_name for item in evidence if item.has_value}
    present = tuple(field for field in required if field in present_names)
    missing = tuple(field for field in required if field not in present_names)
    score = len(present) / len(required) if required else 0.0
    return EvidenceCompleteness(required, present, missing, score)


def build_evidence_trail(
    required_fields: list[str] | tuple[str, ...],
    evidence: list[EvidenceItem] | tuple[EvidenceItem, ...],
    rule_id: str | None = None,
    rule_version: str | None = None,
    comparator: dict[str, Any] | None = None,
    calculation: dict[str, Any] | None = None,
    verdict: str | None = None,
) -> EvidenceTrail:
    return EvidenceTrail(
        evidence=tuple(evidence),
        rule_id=rule_id,
        rule_version=rule_version,
        comparator=comparator,
        calculation=calculation,
        verdict=verdict,
        completeness=calculate_completeness(required_fields, evidence),
    )
