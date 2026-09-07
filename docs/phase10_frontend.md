# Phase 10: Frontend Verification Workflow

The React frontend now provides the first usable ClaimCheck workflow:

1. Enter a barcode and retrieve Open Food Facts product data.
2. Inspect and correct product name, nutrition values, ingredients, and claim text.
3. Normalize the claim through the backend ontology endpoint.
4. Select the comparator state explicitly during review.
5. Submit structured evidence to the deterministic verification endpoint.
6. Inspect verdict, rule ID/version, calculation, completeness, and missing evidence.

The frontend contains no regulatory thresholds and does not calculate compliance. It renders the backend verdict and evidence trail. Empty nutrition fields remain absent from the request. API connection errors are shown to the reviewer and never converted into a verdict.

The PWA manifest and service worker are intentionally deferred to Phase 11.
