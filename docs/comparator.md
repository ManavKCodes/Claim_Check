# Comparator Resolution

Comparative claims require a reference product. Candidate matching considers product category, food type, product family, brand/product identity, serving or per-100g basis, nutrient availability, and source quality.

The resolver returns exactly one status:

- `MATCHED`: one candidate passes all compatibility checks.
- `NO_VALID_COMPARATOR`: no candidate passes.
- `AMBIGUOUS_COMPARATOR`: multiple candidates remain and deterministic selection is not justified.

`NO_VALID_COMPARATOR` and `AMBIGUOUS_COMPARATOR` both lead to `INSUFFICIENT_EVIDENCE`. A candidate rank may be recorded for review, but ranking is not permission to silently select an incompatible product. Subject and reference values must use compatible units and basis before percentage calculations.
