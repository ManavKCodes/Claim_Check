# Phase 1: Requirements and Architecture

## Outcome

Phase 1 establishes the contracts that later implementation phases must honor:

1. Requirements and acceptance boundaries
2. Requirement-to-feature traceability
3. System architecture and data flow
4. Relational data model
5. Extensible claim ontology
6. Versioned rule representation
7. Deterministic rule-engine contract
8. Comparator resolution contract
9. Evidence model
10. Testing and evaluation strategy

## Explicit phase boundary

This phase does not claim that the API, database migrations, frontend, PWA, Open Food Facts client, benchmark, baselines, or deployment already exist. Those are Phase 2 onward deliverables. Any threshold not verified against a supplied FSSAI source remains `PENDING_SOURCE_VERIFICATION`.

## Decision log

| Decision | Rationale |
| --- | --- |
| Python backend with FastAPI | Typed request/response contracts and straightforward testing for a college project |
| React + TypeScript frontend | Responsive UI, installable PWA support, and maintainable form workflows |
| PostgreSQL in deployment, SQLite for local development | Relational integrity with low-friction local setup |
| Versioned JSON rule seeds plus relational Rule records | Reviewable source files and queryable runtime rules |
| Deterministic Python rule engine | Identical inputs and rule versions produce identical verdicts |
| Open Food Facts behind an adapter | Product source can be replaced without changing verification logic |
