# Phase 13: Baselines and Evaluation

## Metrics

The evaluation module reports verdict accuracy, supported-claim precision/recall/F1, false approval rate, false rejection rate, abstention coverage, incorrect abstention rate, and a three-class confusion matrix. Empty inputs return null metrics rather than zero scores.

False approval is counted separately: an expected non-`SUPPORTED` claim predicted as `SUPPORTED`. Abstention coverage counts correctly predicted `INSUFFICIENT_EVIDENCE` cases; incorrect abstentions are tracked separately.

## Baselines

Baseline 1, `ocr_keyword_rules`, reuses claim aliases as a stand-in for OCR text plus keyword rules. It never invents regulatory thresholds and abstains when rule/evidence requirements are unavailable.

Baseline 2, `general_multimodal_llm`, is an explicit adapter boundary. It raises a configuration error until an external model is selected and its predictions are recorded against the same benchmark. No LLM output can enter the deterministic verification engine as a verdict override.

## Measurement status

`POST /api/evaluation/run` reads `BENCHMARK_PATH`. The current benchmark is empty, so the endpoint returns `NOT_YET_MEASURED`. No accuracy, precision, recall, F1, or false-approval result is claimed.
