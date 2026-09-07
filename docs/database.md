# Phase 3: Database and Data Models

## Storage strategy

ClaimCheck uses SQLAlchemy 2.0 models with PostgreSQL as the deployment database and SQLite as the local default. The database URL is supplied through `DATABASE_URL`; no credentials are embedded in source. `app.database.Base.metadata.create_all` is available for local bootstrap and will be replaced or supplemented by reviewed migrations before production deployment.

## Tables

The model layer implements the Phase 1 entity contract:

- `products`, `product_images`, `nutrition_data`, and `ingredients` preserve product facts and their provenance.
- `claims` preserves raw claim text, normalized type, extraction method, confidence, and correction state.
- `rules` stores version, source, threshold metadata, evidence requirements, and explicit source-verification status.
- `comparators` stores subject/reference links, resolution status, matching factors, and basis.
- `verifications` stores the selected rule, comparator, calculation, verdict, completeness, and missing evidence.
- `evidence` stores field-level raw and normalized values connected to a verification.
- `benchmark_records` and `evaluation_results` support manually checked evaluation without fabricating results.

## Integrity rules

- Foreign keys preserve relationships between evidence, verification, claims, products, rules, and comparators.
- Product images, nutrition records, ingredients, claims, and verification evidence are deleted with their parent record.
- Nutrition values are nullable because missing evidence must remain missing rather than become zero.
- Rule thresholds are nullable because unverified FSSAI requirements must remain pending.
- Comparator references are nullable because unresolved comparison must be representable as abstention.
- Indexes cover barcode, product classification, nutrient lookup, claim type, verdict, and verification retrieval.
