# Phase 8: Evidence Trail

Phase 8 adds the evidence-domain service above the relational records introduced in Phase 3. `EvidenceItem` preserves source type, source reference, image reference, field name, raw value, normalized value, unit, extraction method, confidence, and creation time.

`calculate_completeness` compares required evidence keys with evidence items that actually contain a raw or normalized value. Missing evidence remains missing; it is never converted to zero. Duplicate required keys are deduplicated while preserving order.

`EvidenceTrail` groups field evidence with selected rule ID/version, comparator information, calculation, verdict, and completeness. The `POST /api/evidence/completeness` endpoint exposes only completeness data. It does not select rules, resolve comparators, or generate verdicts.
