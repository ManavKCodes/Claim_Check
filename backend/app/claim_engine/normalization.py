import re
import unicodedata

from app.claim_engine.ontology.catalog import CLAIM_CATALOG, ClaimDefinition


def normalize_claim_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    normalized = normalized.replace("%", " percent ")
    return re.sub(r"[^a-z0-9]+", " ", normalized).strip()


def find_claim_definition(value: str) -> ClaimDefinition | None:
    normalized_value = normalize_claim_text(value)
    matches = {
        definition
        for definition in CLAIM_CATALOG
        if any(normalize_claim_text(alias) in normalized_value for alias in definition.aliases)
    }
    return next(iter(matches)) if len(matches) == 1 else None
