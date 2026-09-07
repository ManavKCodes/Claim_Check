from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
import hashlib
import json
from typing import Any

from app.evidence.trail import EvidenceItem, EvidenceTrail, build_evidence_trail
from app.rule_engine.evaluator import EvidenceValue, evaluate_rule
from app.rule_engine.rules.catalog import RuleDefinition, select_rule
from app.rule_engine.verdict import EvaluationResult, Verdict


@dataclass(frozen=True)
class VerificationResult:
    verification_id: str
    claim_type: str
    rule: RuleDefinition | None
    evaluation: EvaluationResult
    trail: EvidenceTrail


def verify_claim(
    claim_type: str,
    raw_claim: str,
    evidence: list[EvidenceItem],
    comparator_status: str | None = None,
    comparator_details: dict[str, Any] | None = None,
) -> VerificationResult:
    rule = select_rule(claim_type)
    if rule is None:
        evaluation = EvaluationResult(
            verdict=Verdict.INSUFFICIENT_EVIDENCE,
            rule_id="NO_APPLICABLE_RULE",
            calculation=None,
            missing_evidence=("applicable_rule",),
            evidence_completeness=0.0,
        )
        trail = build_evidence_trail(["claim", "applicable_rule"], evidence, verdict=evaluation.verdict)
        return _result(claim_type, raw_claim, rule, evaluation, trail)

    if rule.applicable_conditions.get("requires_comparator") and comparator_status != "MATCHED":
        evaluation = EvaluationResult(
            verdict=Verdict.INSUFFICIENT_EVIDENCE,
            rule_id=rule.rule_id,
            calculation=None,
            missing_evidence=("valid_comparator",),
            evidence_completeness=0.0,
        )
    else:
        structured_evidence = _structured_evidence(evidence)
        structured_evidence["claim"] = raw_claim
        structured_evidence["applicable_rule"] = rule.rule_id
        if comparator_status == "MATCHED":
            structured_evidence["reference_product"] = comparator_details or "matched_reference"
            structured_evidence["comparable_basis"] = comparator_details.get("basis", "matched") if comparator_details else "matched"
        evaluation = evaluate_rule(rule, structured_evidence)

    required = list(rule.evidence_requirements)
    if evaluation.missing_evidence:
        required.extend(evaluation.missing_evidence)
    trail = build_evidence_trail(
        required,
        evidence,
        rule_id=rule.rule_id,
        rule_version=rule.regulation_version,
        comparator=comparator_details,
        calculation=evaluation.calculation,
        verdict=evaluation.verdict,
    )
    return _result(claim_type, raw_claim, rule, evaluation, trail)


def _structured_evidence(evidence: list[EvidenceItem]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for item in evidence:
        if item.normalized_value is None:
            result[item.field_name] = item.raw_value
            continue
        if item.field_name.startswith(("subject_", "reference_")):
            try:
                result[item.field_name] = EvidenceValue(
                    value=Decimal(item.normalized_value), unit=item.unit or "", basis="unknown"
                )
                continue
            except (InvalidOperation, TypeError, ValueError):
                pass
        result[item.field_name] = item.normalized_value
    return result


def _result(
    claim_type: str,
    raw_claim: str,
    rule: RuleDefinition | None,
    evaluation: EvaluationResult,
    trail: EvidenceTrail,
) -> VerificationResult:
    identity = {
        "claim_type": claim_type,
        "raw_claim": raw_claim,
        "rule_id": evaluation.rule_id,
        "missing_evidence": evaluation.missing_evidence,
    }
    verification_id = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:24]
    return VerificationResult(verification_id, claim_type, rule, evaluation, trail)
