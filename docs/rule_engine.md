# Rule Engine Design

## Rule contract

Each rule record must contain:

`rule_id`, `claim_type`, `regulation_name`, `regulation_version`, `effective_date`, `nutrient`, `threshold`, `threshold_type`, `unit`, `applicable_conditions`, `calculation_method`, `evidence_requirements`, `source_reference`, and `notes`.

Rules are loaded by version and selected by claim type plus applicable product basis. A rule without a verified source is unavailable for production verification and yields `INSUFFICIENT_EVIDENCE`.

## Evaluation pipeline

1. Validate claim ontology type.
2. Select one applicable sourced rule.
3. Validate every required evidence element.
4. Reject missing, invalid, incompatible, or ambiguous values.
5. Normalize units and product basis.
6. Calculate using typed deterministic calculators.
7. Compare against the rule, including boundaries explicitly.
8. Emit calculation, evidence completeness, and one of the three verdicts.

Missing evidence is never interpreted as zero. Comparative calculations reject a zero or missing reference denominator. The engine has no LLM dependency and exposes no override hook.

## Rule status

FSSAI Advertising and Claims Regulations and current FSSAI Labelling and Display Regulations are the intended sources. Exact threshold values, versions, effective dates, and interpretations are `PENDING_SOURCE_VERIFICATION` until checked against authoritative documents.
