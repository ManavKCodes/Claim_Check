import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RuleDefinition:
    rule_id: str
    claim_type: str
    regulation_name: str
    regulation_version: str
    effective_date: str | None
    nutrient: str | None
    threshold: Decimal | None
    threshold_type: str | None
    unit: str | None
    applicable_conditions: dict[str, Any]
    calculation_method: str
    evidence_requirements: tuple[str, ...]
    source_reference: str
    notes: str | None
    status: str


def load_rule_catalog() -> tuple[RuleDefinition, ...]:
    source = Path(__file__).with_name("fssai_rules.json")
    records = json.loads(source.read_text(encoding="utf-8"))
    return tuple(
        RuleDefinition(
            rule_id=record["rule_id"],
            claim_type=record["claim_type"],
            regulation_name=record["regulation_name"],
            regulation_version=record["regulation_version"],
            effective_date=record["effective_date"],
            nutrient=record["nutrient"],
            threshold=Decimal(str(record["threshold"])) if record["threshold"] is not None else None,
            threshold_type=record["threshold_type"],
            unit=record["unit"],
            applicable_conditions=record["applicable_conditions"],
            calculation_method=record["calculation_method"],
            evidence_requirements=tuple(record["evidence_requirements"]),
            source_reference=record["source_reference"],
            notes=record["notes"],
            status=record["status"],
        )
        for record in records
    )


RULE_CATALOG = load_rule_catalog()
RULE_BY_CLAIM_TYPE = {rule.claim_type: rule for rule in RULE_CATALOG}


def select_rule(claim_type: str) -> RuleDefinition | None:
    return RULE_BY_CLAIM_TYPE.get(claim_type)
