from dataclasses import dataclass

from app.claim_engine.extraction import extract_claim
from app.rule_engine.verdict import Verdict


@dataclass(frozen=True)
class BaselinePrediction:
    baseline_name: str
    claim_type: str | None
    verdict: Verdict
    notes: str


def ocr_keyword_baseline(raw_text: str) -> BaselinePrediction:
    """Baseline 1: extracted text plus aliases, with no regulatory guessing."""
    claim = extract_claim(raw_text, source="ocr_keyword_baseline")
    if claim.claim_type is None:
        return BaselinePrediction("ocr_keyword_rules", None, Verdict.INSUFFICIENT_EVIDENCE, "Claim keyword was unknown or ambiguous.")
    return BaselinePrediction(
        "ocr_keyword_rules",
        claim.claim_type,
        Verdict.INSUFFICIENT_EVIDENCE,
        "Threshold and required evidence are unavailable to this baseline.",
    )


class MultimodalBaseline:
    """Baseline 2 adapter; an external model must provide a recorded prediction."""

    name = "general_multimodal_llm"

    def predict(self, evidence_reference: str) -> BaselinePrediction:
        raise NotImplementedError(
            "Configure an external multimodal model and record predictions on the same benchmark before evaluation."
        )
