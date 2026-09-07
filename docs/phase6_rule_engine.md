# Phase 6: FSSAI Rules and Deterministic Rule Engine

## Rule catalog

The catalog contains one structured rule record for each supported claim. Every record includes the required rule metadata, source reference, evidence requirements, calculation method, and status. All current records are `PENDING_SOURCE_VERIFICATION`; thresholds and effective dates are null until authoritative FSSAI documents are reviewed. This is intentional and prevents fabricated regulatory requirements.

## Engine behavior

`evaluate_rule` validates rule status, required evidence, units, numeric values, and comparison basis before calculating. It returns exactly one `Verdict`: `SUPPORTED`, `CONTRADICTED`, or `INSUFFICIENT_EVIDENCE`.

The engine supports numeric threshold rules and comparative percentage calculations. It handles equality boundaries, invalid/missing values, incompatible units, missing reference values, and zero reference values. Missing evidence is never treated as zero. A pending rule always abstains, even when label evidence exists.

Synthetic verified rules appear only in tests to exercise calculation behavior. They are not FSSAI claims or production thresholds.
