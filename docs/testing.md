# Testing Strategy

## Test layers

- Unit: ontology normalization, unit conversion, calculators, validators, verdict mapping, completeness.
- Rule-engine: below, equal, above, missing, invalid, wrong-unit, and boundary cases for every claim rule.
- Comparator: matched, no match, ambiguous, missing reference value, zero denominator, incompatible basis, and percentage boundaries.
- Integration: product adapter, persistence, rule selection, evidence creation, and verification orchestration.
- API: validation, error responses, classification, analysis, verification, evaluation, and exactly three verdict values.
- End-to-end: supported, contradicted, and insufficient-evidence demonstrations in `test_end_to_end_cases.py`; verified test rules are synthetic and never presented as FSSAI measurements.
- Evaluation: metric formulas, brand/product-family split, and no fabricated result behavior.

## Mandatory invariants

1. Missing nutrition never becomes zero.
2. The UI cannot provide a verdict independently of the backend engine.
3. A missing or ambiguous comparator abstains.
4. Identical normalized input and rule version are deterministic.
5. Every verdict has an inspectable evidence trail.

The backend suite is now distributed across unit, API, comparator, evidence, evaluation, and mandatory case tests. Runtime execution still depends on installing Python dependencies.
