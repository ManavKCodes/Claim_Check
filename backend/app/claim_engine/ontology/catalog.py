import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ClaimDefinition:
    claim_type: str
    display_name: str
    category: str
    nutrient: str
    requires_comparator: bool
    required_evidence: tuple[str, ...]
    aliases: tuple[str, ...]


def load_claim_catalog() -> tuple[ClaimDefinition, ...]:
    source = Path(__file__).with_name("claim_ontology.json")
    records = json.loads(source.read_text(encoding="utf-8"))
    return tuple(
        ClaimDefinition(
            claim_type=record["claim_type"],
            display_name=record["display_name"],
            category=record["category"],
            nutrient=record["nutrient"],
            requires_comparator=record["requires_comparator"],
            required_evidence=tuple(record["required_evidence"]),
            aliases=tuple(record["aliases"]),
        )
        for record in records
    )


CLAIM_CATALOG = load_claim_catalog()
CLAIM_BY_TYPE = {definition.claim_type: definition for definition in CLAIM_CATALOG}
