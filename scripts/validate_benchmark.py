"""Validate manually annotated ClaimCheck benchmark records."""

import json
from pathlib import Path
import sys


CLAIM_TYPES = {"HIGH_PROTEIN", "LOW_FAT", "NO_ADDED_SUGAR", "COMPARATIVE_PROTEIN", "REDUCED_SODIUM"}
VERDICTS = {"SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE"}


def validate_record(record: dict[str, object], index: int) -> list[str]:
    errors: list[str] = []
    required = ("record_id", "product_image", "product_name", "brand", "category", "raw_claim", "claim_type", "nutrition", "rule_id", "expected_verdict", "evidence_notes", "annotation_notes", "split_group", "split")
    for field in required:
        if not record.get(field):
            errors.append(f"record {index}: missing {field}")
    if record.get("claim_type") not in CLAIM_TYPES:
        errors.append(f"record {index}: unsupported claim_type")
    if record.get("expected_verdict") not in VERDICTS:
        errors.append(f"record {index}: unsupported expected_verdict")
    if record.get("split") not in {"train", "test"}:
        errors.append(f"record {index}: split must be train or test")
    if not isinstance(record.get("nutrition"), dict):
        errors.append(f"record {index}: nutrition must be an object")
    return errors


def validate(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("records")
    if not isinstance(records, list):
        return ["records must be an array"]
    errors: list[str] = []
    ids: set[str] = set()
    groups: dict[str, str] = {}
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"record {index}: must be an object")
            continue
        errors.extend(validate_record(record, index))
        record_id = record.get("record_id")
        if isinstance(record_id, str) and record_id in ids:
            errors.append(f"record {index}: duplicate record_id")
        if isinstance(record_id, str):
            ids.add(record_id)
        group, split = record.get("split_group"), record.get("split")
        if isinstance(group, str) and isinstance(split, str):
            previous = groups.setdefault(group, split)
            if previous != split:
                errors.append(f"record {index}: split leakage for group {group}")
    return errors


if __name__ == "__main__":
    benchmark_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/benchmark/records.json")
    problems = validate(benchmark_path)
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)
    print(f"Benchmark valid: {benchmark_path}")
