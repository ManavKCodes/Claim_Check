# ClaimCheck

ClaimCheck is an evidence-screening tool for nutrition and comparative claims printed on packaged food sold in India. It combines product evidence, a claim ontology, versioned FSSAI rules, comparator resolution, evidence provenance, and deterministic verification.

**ClaimCheck is an evidence-screening tool and not a legal certification.** Open Food Facts is used as a product-data source. FSSAI is the regulatory authority.

## Problem statement

Packaged-food claims can be difficult to check from a label alone. ClaimCheck helps a reviewer identify the product, inspect extracted evidence, correct fields, resolve a valid comparator where required, and see why a claim is supported, contradicted, or left unresolved.

## Key features

- Barcode/product lookup through an Open Food Facts adapter.
- Machine-readable, extensible claim ontology.
- Versioned FSSAI rule records with source status.
- Deterministic numeric and comparative calculations.
- Comparator matching with explicit abstention.
- Field-level evidence trail and completeness score.
- Reviewable responsive frontend and installable PWA shell.
- Benchmark annotation, leakage prevention, metrics, and baseline boundaries.

## Supported claims

1. High Protein (`HIGH_PROTEIN`)
2. Low Fat (`LOW_FAT`)
3. No Added Sugar (`NO_ADDED_SUGAR`)
4. 30% More Protein (`COMPARATIVE_PROTEIN`)
5. Reduced Sodium (`REDUCED_SODIUM`)

## Architecture

```text
Product source -> claim extraction -> ontology -> comparator (if needed)
			   -> FSSAI rule selection -> evidence validation
			   -> deterministic calculation -> verdict and evidence trail
```

The repository separates `backend`, `frontend`, `claim_engine`, `rule_engine`, `comparator`, `evidence`, `evaluation`, `data`, `tests`, `docs`, and `config`. See [docs/architecture.md](docs/architecture.md).

### Claim ontology

Ontology metadata contains claim type, display name, category, nutrient, comparator requirement, aliases, and required evidence. It is defined in [claim_ontology.json](backend/app/claim_engine/ontology/claim_ontology.json), not in UI threshold logic.

### FSSAI rule engine

Rule records contain rule ID, regulation/version, nutrient, threshold metadata, conditions, calculation method, evidence requirements, source, and status. Current thresholds are deliberately `PENDING_SOURCE_VERIFICATION`; no regulatory threshold is fabricated.

### Comparator resolution

Comparative claims require a compatible reference product. The resolver returns `MATCHED`, `NO_VALID_COMPARATOR`, or `AMBIGUOUS_COMPARATOR`; unresolved cases abstain.

### Evidence trail

Evidence preserves source type/reference, image reference, raw and normalized values, units, extraction method, confidence, timestamps, selected rule/version, comparator, calculation, missing fields, and final verdict.

### ML/AI role

AI/ML may later assist extraction, classification, candidate ranking, or explanation. It cannot select or override the final deterministic verdict.

## Verdicts

Every verification returns exactly one of:

- `SUPPORTED`
- `CONTRADICTED`
- `INSUFFICIENT_EVIDENCE`

Missing, invalid, ambiguous, or unavailable evidence never becomes zero and never becomes approval.

## Benchmark and evaluation

The planned benchmark is approximately 150–200 manually checked Indian packaged-food products. Records include images, product identity, claim text/type, nutrition, rule, comparator, expected verdict, evidence notes, and annotation notes. Splits are by brand or product family to prevent leakage; they are not random row splits.

Metrics include OCR field accuracy, claim extraction precision/recall, classification F1, verdict accuracy, false approval/rejection rates, abstention coverage, incorrect abstention, confusion matrix, and evidence completeness. The current benchmark is empty, so all real measurements are **NOT YET MEASURED**.

Baseline 1 is an OCR/keyword boundary. Baseline 2 is an external multimodal-model adapter. Both must use the same benchmark before comparison.

## Project status

**Implemented:** backend/frontend foundation, ontology, Open Food Facts adapter, rule/evidence/comparator modules, API orchestration, PWA packaging, annotation schema, metric functions, CI configuration, and Render blueprint.

**Verified:** backend tests (45 passed), frontend typecheck/build, Playwright E2E (2 passed), local PWA shell/manifest/service-worker behavior, and static secret/configuration checks.

**Not yet verified:** Docker image/Compose launch, public HTTPS deployment, live Open Food Facts production behavior, and hosted PWA installation.

**Requires real benchmark data:** 150–200 annotations, leakage-reviewed splits, accuracy/precision/recall/F1, false approval/rejection, abstention, OCR metrics, and baseline comparison.

**Requires manual action:** authoritative FSSAI source verification, GitHub push, Render service creation/configuration, production secrets, and public URL verification.

## LIVE DEMO

URL: **NOT DEPLOYED**

## Installation and local development

Backend with Python 3.12:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
$env:PYTHONPATH = "backend"
uvicorn app.main:app --reload --port 8000
```

Frontend with Node.js 22+:

```powershell
cd frontend
npm ci
npm run dev
```

Copy `.env.example` to `.env` and replace local values. Never commit `.env`.

## Testing

```powershell
.venv\Scripts\python.exe -m pytest backend/tests -q
cd frontend
npm run typecheck
npm run build
npm run test:e2e
```

The E2E command requires `npx playwright install chromium` once.

## Deployment

The full-stack local profile is defined in [docker-compose.yml](docker-compose.yml). Render preparation is in [render.yaml](render.yaml) and [docs/deployment.md](docs/deployment.md). Set `VITE_API_URL`, `ALLOWED_ORIGINS`, `DATABASE_URL`, and the Open Food Facts User-Agent through the hosting provider’s environment configuration.

GitHub Pages cannot host the complete application because verification and product lookup require the backend. Use a full-stack host such as Render for the API/database and frontend.

## Limitations

- FSSAI thresholds are pending authoritative source verification.
- The benchmark is empty and results are not measured.
- The multimodal baseline is not configured.
- Docker and public deployment require manual environment/hosting setup.
- Open Food Facts data availability and label completeness vary by product.

## Documentation

See [docs/requirements_traceability.md](docs/requirements_traceability.md), [docs/final_audit.md](docs/final_audit.md), and the phase documents under `docs/`.
