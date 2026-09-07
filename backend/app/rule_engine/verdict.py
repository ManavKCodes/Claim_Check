from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class Verdict(StrEnum):
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass(frozen=True)
class EvaluationResult:
    verdict: Verdict
    rule_id: str
    calculation: dict[str, Any] | None
    missing_evidence: tuple[str, ...]
    evidence_completeness: float
