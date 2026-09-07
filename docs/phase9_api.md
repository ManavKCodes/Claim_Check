# Phase 9: Backend API Orchestration

Phase 9 connects the existing modules through typed FastAPI endpoints:

- `POST /api/product/analyze` creates a structured claim candidate from product context.
- `POST /api/claim/classify` returns ontology metadata for a claim candidate.
- `POST /api/comparator/resolve` is provided by Phase 7.
- `POST /api/evidence/completeness` is provided by Phase 8.
- `POST /api/verify` runs evidence through comparator gating, rule selection, deterministic evaluation, and evidence-trail assembly.

Verification IDs are deterministic hashes of the normalized claim identity, selected rule identity, and missing evidence. The current production rule catalog is pending source verification, so the API conservatively returns `INSUFFICIENT_EVIDENCE` until authoritative FSSAI thresholds are verified. No LLM is used to select a verdict.

Database-backed verification retrieval endpoints and persistence orchestration remain later integration work; this phase does not claim those are implemented.
