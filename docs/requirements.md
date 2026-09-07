# Requirements

## Functional requirements

| ID | Requirement | Acceptance criterion |
| --- | --- | --- |
| FR-01 | Accept barcode, product link, and product/label evidence | A verification request can identify a product or safely abstain |
| FR-02 | Support five claim types | Each claim maps to ontology metadata, not UI-specific logic |
| FR-03 | Use Open Food Facts as a product-data source | Access is isolated behind `OpenFoodFactsClient` with attribution and rate limits |
| FR-04 | Use versioned FSSAI rules | Every evaluation records rule ID, version, and source |
| FR-05 | Resolve comparators | Comparative claims require a matched, comparable reference or abstain |
| FR-06 | Verify deterministically | The rule engine, not an LLM, selects the final verdict |
| FR-07 | Produce an evidence trail | Users can inspect source, values, rule, calculation, and missing evidence |
| FR-08 | Allow correction | Extracted fields can be reviewed and corrected before verification |
| FR-09 | Expose exactly three verdicts | No probabilistic final labels are returned |
| FR-10 | Evaluate performance | Benchmark tooling reports extraction, classification, verdict, abstention, and evidence metrics |

## Non-functional requirements

- Conservative failure: missing, invalid, ambiguous, or stale evidence returns `INSUFFICIENT_EVIDENCE`.
- Reproducibility: identical normalized input and rule version produce identical output.
- Security: validate URLs, barcodes, uploads, request sizes, CORS, and secrets.
- Auditability: structured logs and immutable verification evidence are retained.
- Accessibility and responsiveness: the web UI works on desktop, tablet, and mobile.
- Maintainability: claim, rule, comparator, and evidence modules remain independently testable.
