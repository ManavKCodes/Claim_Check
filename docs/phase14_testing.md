# Phase 14: Testing

Phase 14 adds API contract tests and the three mandatory demonstration cases:

1. A supported claim using a synthetic verified test rule.
2. A contradicted claim using a synthetic verified test rule.
3. An insufficient comparative claim with no valid comparator.

Production FSSAI rules remain pending source verification. The supported and contradicted unit cases therefore use isolated synthetic rule copies only to exercise deterministic calculation behavior; they are not benchmark results or regulatory conclusions.

The API tests verify claim classification, product analysis provenance, evidence-backed verification responses, and empty-benchmark evaluation status. The frontend Playwright suite covers the review workflow and ensures API failures do not become verdicts. The backend suite passed with 44 tests, and the Playwright suite passed with 2 tests using Chromium 131.
