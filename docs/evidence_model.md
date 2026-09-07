# Evidence Model

## Evidence

```text
id, verification_id, source_type, source_reference, image_reference,
field_name, raw_value, normalized_value, unit, extraction_method,
confidence, created_at
```

`source_type` distinguishes Open Food Facts, packaging image, user correction, benchmark annotation, and regulatory source. User corrections preserve the previous value as provenance rather than overwriting history.

## Verification

```text
id, product_id, claim_id, rule_id, comparator_id, calculation,
verdict, evidence_completeness, missing_evidence, created_at
```

Every result page must expose the raw claim, extracted and normalized values, subject/reference products, selected rule and version, calculation, evidence status, missing elements, and final verdict. Completeness is an indicator of required evidence presence; it never replaces the verdict.
