# Phase 5: Claim Extraction and Normalization

The claim ontology is stored in `backend/app/claim_engine/ontology/claim_ontology.json`. Each definition includes the normalized claim type, display name, category, nutrient, comparator requirement, required evidence keys, and approved aliases. Regulatory thresholds do not belong in this catalog.

The current extractor is deterministic and alias-based. It preserves raw input, source, extraction method, normalized claim type, and an explicit confidence value. A known alias maps to exactly one ontology definition. Unknown text and text containing multiple supported claim types remain unclassified instead of being guessed.

This module creates structured claim candidates only. It cannot select FSSAI rules, resolve comparators, or produce `SUPPORTED`, `CONTRADICTED`, or `INSUFFICIENT_EVIDENCE`.

The API endpoint is `POST /api/claim/extract` with `raw_text` and `source`. User correction and image/OCR-assisted candidate generation will be integrated later, while retaining this ontology validation boundary.
