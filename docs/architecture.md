# Architecture

## System flow

```text
Input -> Product identification -> Packaging/product evidence
      -> Claim extraction and normalization -> Claim ontology
      -> Comparator resolution when required -> FSSAI rule selection
      -> Evidence validation -> Unit normalization -> Calculation
      -> Deterministic verdict -> Evidence trail and UI result
```

The frontend never decides compliance. The backend orchestrates modules and persists the evidence required to reproduce a result.

## Target folder structure

```text
claimcheck/
├── backend/              # FastAPI routes, services, persistence
├── frontend/             # React/TypeScript responsive PWA
├── claim_engine/         # extraction, classification, normalization
├── rule_engine/          # ontology, rules, evaluators, calculators, verdict
├── comparator/           # candidate filtering and resolution
├── evidence/             # evidence contracts and completeness
├── data/                 # benchmark, annotations, verified samples
├── evaluation/           # metrics and baseline runners
├── tests/                # unit, integration, API, and E2E tests
├── docs/                 # requirements and engineering documentation
├── scripts/              # migrations, seed, benchmark utilities
└── config/               # non-secret project contracts and rule seeds
```

## Database design

`Product` has many `ProductImage`, `NutritionData`, and `Ingredient` records. `Claim` belongs to a product and preserves raw text plus normalized ontology type. `Rule` is versioned and selected by claim type. `Comparator` links a subject product and reference product and records resolution status. `Verification` links product, claim, rule, optional comparator, calculation, verdict, and completeness. `Evidence` belongs to a verification and records source, raw/normalized value, unit, extraction method, and confidence. `BenchmarkRecord` stores manually checked expected results; `EvaluationResult` stores measured metrics and dataset split metadata.

## Separation of responsibilities

- Product adapters retrieve external product facts only.
- Claim processing creates structured candidates only.
- Rule engine validates and calculates only from structured evidence.
- Comparator module can abstain and never silently picks a candidate.
- Persistence stores provenance and does not alter verdict semantics.
- Frontend renders and edits structured fields; it does not contain thresholds.
