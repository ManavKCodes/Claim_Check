from dataclasses import dataclass

from app.claim_engine.normalization import find_claim_definition


@dataclass(frozen=True)
class ExtractedClaim:
    raw_claim: str
    normalized_claim: str | None
    claim_type: str | None
    extraction_method: str
    confidence: float | None
    source: str


def extract_claim(raw_text: str, source: str = "user_input") -> ExtractedClaim:
    raw_claim = raw_text.strip()
    if not raw_claim:
        return ExtractedClaim(raw_text, None, None, "deterministic_alias", None, source)
    definition = find_claim_definition(raw_claim)
    if definition is None:
        return ExtractedClaim(raw_claim, None, None, "deterministic_alias", None, source)
    return ExtractedClaim(
        raw_claim=raw_claim,
        normalized_claim=definition.claim_type,
        claim_type=definition.claim_type,
        extraction_method="deterministic_alias",
        confidence=1.0,
        source=source,
    )
