import json
from pathlib import Path
from typing import Any

from app.evaluation.baselines import ocr_keyword_baseline
from app.evaluation.metrics import evaluate_verdicts, metric_dict


def load_benchmark(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError("Benchmark records must be an array")
    return records


def run_evaluation(path: Path) -> dict[str, object]:
    records = load_benchmark(path)
    if not records:
        return {"status": "NOT_YET_MEASURED", "reason": "Benchmark contains no manually checked records.", "sample_count": 0}
    expected = [record["expected_verdict"] for record in records]
    baseline_predictions = [ocr_keyword_baseline(record["raw_claim"]).verdict.value for record in records]
    metrics = evaluate_verdicts(expected, baseline_predictions)
    return {"status": "MEASURED", "sample_count": len(records), "baseline": "ocr_keyword_rules", "metrics": metric_dict(metrics)}
