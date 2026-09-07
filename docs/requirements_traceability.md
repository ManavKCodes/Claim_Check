# Requirements Traceability

| Requirement | Implementation target | Module/document | Test | Status |
| --- | --- | --- | --- | --- |
| Five supported claims | Configuration-driven ontology | `claim_engine`, [claim_ontology.md](claim_ontology.md) | Ontology coverage tests | DESIGNED |
| Three verdict states | Enum and verdict engine | `rule_engine/verdict` | Verdict enum tests | DESIGNED |
| Open Food Facts source | Adapter with attribution/rate limits | `backend/product_sources` | Adapter contract tests | DESIGNED |
| Product lookup integration | Validated barcode/URL lookup and normalized source response | `backend/app/product_sources/open_food_facts.py`, `backend/app/main.py` | `backend/tests/test_open_food_facts.py` | IMPLEMENTED (PHASE 4) |
| Claim ontology and normalization | Machine-readable five-claim catalog and deterministic extractor | `backend/app/claim_engine`, `backend/app/schemas.py` | `backend/tests/test_claim_engine.py` | IMPLEMENTED (PHASE 5) |
| Versioned FSSAI rules | Structured pending-source rule catalog and selector | `backend/app/rule_engine/rules` | `backend/tests/test_rule_engine.py` | IMPLEMENTED (PHASE 6) |
| Deterministic rule evaluation | Typed numeric/comparative evaluator with conservative abstention | `backend/app/rule_engine/evaluator.py`, `backend/app/rule_engine/verdict.py` | `backend/tests/test_rule_engine.py` | IMPLEMENTED (PHASE 6) |
| Comparator resolution | Compatibility filtering and explicit matched/no-valid/ambiguous results | `backend/app/comparator/resolver.py` | `backend/tests/test_comparator.py` | IMPLEMENTED (PHASE 7) |
| Evidence trail | Provenance contracts, evidence completeness, and trail assembly | `backend/app/evidence/trail.py` | `backend/tests/test_evidence.py` | IMPLEMENTED (PHASE 8) |
| Backend API orchestration | Typed product analysis, claim classification, verification, and evidence responses | `backend/app/main.py`, `backend/app/verification/service.py` | `backend/tests/test_verification_service.py` | IMPLEMENTED (PHASE 9) |
| Reviewable frontend workflow | Product lookup, editable claim/evidence fields, verification result view | `frontend/src/main.tsx`, `frontend/src/styles.css` | Frontend typecheck and E2E workflow test | IMPLEMENTED (PHASE 10) |
| Installable PWA | Manifest, icons, production service worker, responsive shell | `frontend/public`, `frontend/index.html`, `frontend/src/main.tsx` | Production build and browser install test | IMPLEMENTED (PHASE 11) |
| Benchmark annotation | Empty benchmark container, annotation template, schema, validator, and split leakage check | `data/benchmark`, `scripts/validate_benchmark.py` | Benchmark validator tests | IMPLEMENTED (PHASE 12) |
| Evaluation metrics and baselines | Metric functions, OCR/keyword baseline, external multimodal adapter, empty benchmark runner | `backend/app/evaluation`, `evaluation`, `backend/tests/test_evaluation.py` | Evaluation metric tests | IMPLEMENTED (PHASE 13) |
| Testing strategy | API contracts, three mandatory demonstration cases, and frontend E2E workflow | `backend/tests`, `frontend/tests`, `frontend/playwright.config.ts` | pytest and Playwright suites | VALIDATED (PHASE 14) |
| Deployment and finalization | Compose services, configurable CORS, frontend API build arg, deployment/runbook docs | `docker-compose.yml`, Dockerfiles, [deployment.md](deployment.md) | Container build and deployment gates | IMPLEMENTED (PHASE 15; NOT DEPLOYED) |
| Versioned FSSAI rules | Rule records with source and version | `rule_engine/rules` | Rule selection tests | DESIGNED |
| Deterministic verification | Typed calculators and validators | `rule_engine` | Boundary and repeatability tests | DESIGNED |
| Comparator resolution | Matched/no-valid/ambiguous statuses | `comparator` | Comparator test matrix | DESIGNED |
| Evidence trail | Evidence and Verification records | `evidence`, [evidence_model.md](evidence_model.md) | Evidence completeness tests | DESIGNED |
| Relational database entities | SQLAlchemy models, session factory, and local database health check | `backend/app/database.py`, `backend/app/models.py`, [database.md](database.md) | Schema/model tests | IMPLEMENTED (PHASE 3) |
| User correction workflow | Editable structured extraction review | `frontend` | UI E2E test | PLANNED |
| Benchmark and annotation process | Manual records with brand split | `data`, `evaluation`, [dataset.md](dataset.md) | Split leakage test | PLANNED |
| Baseline comparison | OCR keyword baseline and multimodal baseline | `evaluation` | Same-benchmark test | PLANNED |
| PWA and responsive website | React app, manifest, service worker | `frontend` | Build and E2E tests | PLANNED |
| Secure configuration | Environment variables, upload validation, CORS | `backend`, `.env.example` | Security/API tests | DESIGNED |
| Documentation and schedule | Engineering docs and 17-week plan | `docs` | Documentation checklist | IN PROGRESS |

Phase 1 status is intentionally not `IMPLEMENTED` for runtime requirements. No benchmark metrics, deployment, or regulatory conclusions are claimed yet.
