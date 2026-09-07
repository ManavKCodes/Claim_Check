# Phase 7: Comparator Resolution

Comparative claims cannot be verified from a subject product alone. The resolver accepts a subject and candidate products and checks product identity, category, product family when available, nutrition basis, nutrient name, unit, and reference value availability.

The resolver returns exactly one of:

- `MATCHED`: exactly one candidate passed all checks and is returned.
- `NO_VALID_COMPARATOR`: no candidate passed, so no reference is returned.
- `AMBIGUOUS_COMPARATOR`: multiple candidates passed, so no reference is returned.

The API endpoint is `POST /api/comparator/resolve`. The resolver does not rank candidates into a silent choice, calculate a verdict, or override the rule engine. `NO_VALID_COMPARATOR` and `AMBIGUOUS_COMPARATOR` must become `INSUFFICIENT_EVIDENCE` when verification orchestration is implemented.
