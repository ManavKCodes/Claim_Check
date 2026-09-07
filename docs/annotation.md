# Phase 12: Benchmark Annotation

The benchmark is intentionally empty in this repository. `data/benchmark/records.json` is a real empty container, not a fabricated dataset or measured result.

## Annotation workflow

1. Inspect the product image and product source record.
2. Transcribe the claim verbatim.
3. Assign one ontology claim type.
4. Record nutrition values, units, basis, and source references.
5. Record the verified rule ID or mark the case insufficient.
6. Resolve and document a comparator when required.
7. Assign the expected verdict from evidence, not intuition.
8. Add evidence and annotation notes.
9. Assign a brand/product-family split group and split.
10. Perform an independent quality review.

## Validation

Run `python scripts/validate_benchmark.py`. The validator checks required fields, supported claim/verdict values, unique record IDs, and prevents the same brand/product-family group from appearing in both train and test.

The target is approximately 150-200 manually checked Indian packaged-food products. Until records are entered and reviewed, benchmark size and all evaluation metrics remain **NOT YET MEASURED**.
