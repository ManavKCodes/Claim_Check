from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from app.rule_engine.rules.catalog import RuleDefinition
from app.rule_engine.verdict import EvaluationResult, Verdict


@dataclass(frozen=True)
class EvidenceValue:
    value: Decimal
    unit: str
    basis: str


def evaluate_rule(rule: RuleDefinition, evidence: dict[str, Any]) -> EvaluationResult:
    required = rule.evidence_requirements
    missing = tuple(field for field in required if field not in evidence or evidence[field] in (None, ""))
    if rule.status != "VERIFIED" or rule.threshold is None or rule.threshold_type is None:
        return _insufficient(rule, missing + ("verified_rule",))
    if missing:
        return _insufficient(rule, missing)
    if rule.calculation_method in {"percentage_difference", "percentage_reduction"}:
        return _evaluate_comparative(rule, evidence)
    return _evaluate_numeric(rule, evidence)


def _evaluate_numeric(rule: RuleDefinition, evidence: dict[str, Any]) -> EvaluationResult:
    evidence_key = f"subject_{rule.nutrient}"
    value = _decimal_evidence(evidence.get(evidence_key))
    if value is None:
        return _insufficient(rule, (evidence_key,))
    if rule.unit and value.unit != rule.unit:
        return _insufficient(rule, (f"compatible_unit:{rule.unit}",))
    calculation = {"method": rule.calculation_method, "value": str(value.value), "threshold": str(rule.threshold)}
    supported = _compare(value.value, rule.threshold, rule.threshold_type)
    return EvaluationResult(
        verdict=Verdict.SUPPORTED if supported else Verdict.CONTRADICTED,
        rule_id=rule.rule_id,
        calculation=calculation,
        missing_evidence=(),
        evidence_completeness=1.0,
    )


def _evaluate_comparative(rule: RuleDefinition, evidence: dict[str, Any]) -> EvaluationResult:
    subject = _decimal_evidence(evidence.get(f"subject_{rule.nutrient}"))
    reference = _decimal_evidence(evidence.get(f"reference_{rule.nutrient}"))
    if subject is None or reference is None:
        missing = tuple(
            key
            for key, value in (
                (f"subject_{rule.nutrient}", subject),
                (f"reference_{rule.nutrient}", reference),
            )
            if value is None
        )
        return _insufficient(rule, missing)
    if reference.value == 0 or subject.unit != reference.unit or (rule.unit and subject.unit != rule.unit):
        return _insufficient(rule, ("valid_comparison_basis",))
    if rule.calculation_method == "percentage_difference":
        percentage = ((subject.value - reference.value) / reference.value) * 100
    else:
        percentage = ((reference.value - subject.value) / reference.value) * 100
    calculation = {"method": rule.calculation_method, "percentage": str(percentage), "threshold": str(rule.threshold)}
    supported = _compare(percentage, rule.threshold, rule.threshold_type)
    return EvaluationResult(
        verdict=Verdict.SUPPORTED if supported else Verdict.CONTRADICTED,
        rule_id=rule.rule_id,
        calculation=calculation,
        missing_evidence=(),
        evidence_completeness=1.0,
    )


def _decimal_evidence(value: Any) -> EvidenceValue | None:
    if not isinstance(value, EvidenceValue):
        return None
    try:
        return EvidenceValue(Decimal(value.value), value.unit, value.basis)
    except (InvalidOperation, TypeError, ValueError):
        return None


def _compare(value: Decimal, threshold: Decimal, threshold_type: str) -> bool:
    if threshold_type == "greater_than_or_equal":
        return value >= threshold
    if threshold_type == "less_than_or_equal":
        return value <= threshold
    if threshold_type == "percentage_at_least":
        return value >= threshold
    return False


def _insufficient(rule: RuleDefinition, missing: tuple[str, ...]) -> EvaluationResult:
    unique_missing = tuple(dict.fromkeys(missing))
    required_count = max(len(rule.evidence_requirements) + 1, 1)
    present_count = max(required_count - len(unique_missing), 0)
    return EvaluationResult(
        verdict=Verdict.INSUFFICIENT_EVIDENCE,
        rule_id=rule.rule_id,
        calculation=None,
        missing_evidence=unique_missing,
        evidence_completeness=present_count / required_count,
    )
