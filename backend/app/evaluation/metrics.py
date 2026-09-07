from collections import Counter
from dataclasses import dataclass


VERDICTS = ("SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE")


@dataclass(frozen=True)
class ClassificationMetrics:
    sample_count: int
    accuracy: float | None
    precision: float | None
    recall: float | None
    f1: float | None
    false_approval_rate: float | None
    false_rejection_rate: float | None
    abstention_coverage: float | None
    incorrect_abstention_rate: float | None
    confusion_matrix: dict[str, dict[str, int]]


def evaluate_verdicts(expected: list[str], predicted: list[str]) -> ClassificationMetrics:
    if len(expected) != len(predicted):
        raise ValueError("Expected and predicted verdict lists must have the same length")
    count = len(expected)
    matrix = {actual: {label: 0 for label in VERDICTS} for actual in VERDICTS}
    for actual, result in zip(expected, predicted):
        if actual not in VERDICTS or result not in VERDICTS:
            raise ValueError("Unknown verdict label")
        matrix[actual][result] += 1
    if count == 0:
        return ClassificationMetrics(0, None, None, None, None, None, None, None, None, matrix)

    supported_actual = matrix["SUPPORTED"]["SUPPORTED"]
    supported_predicted = sum(matrix[actual]["SUPPORTED"] for actual in VERDICTS)
    true_non_supported = count - supported_actual
    false_approval = sum(matrix[actual]["SUPPORTED"] for actual in VERDICTS if actual != "SUPPORTED")
    false_rejection = matrix["SUPPORTED"]["CONTRADICTED"]
    correct_abstentions = matrix["INSUFFICIENT_EVIDENCE"]["INSUFFICIENT_EVIDENCE"]
    incorrect_abstentions = sum(matrix[actual]["INSUFFICIENT_EVIDENCE"] for actual in VERDICTS if actual != "INSUFFICIENT_EVIDENCE")
    precision = supported_actual / supported_predicted if supported_predicted else 0.0
    actual_supported = supported_actual + matrix["SUPPORTED"]["CONTRADICTED"] + matrix["SUPPORTED"]["INSUFFICIENT_EVIDENCE"]
    recall = supported_actual / actual_supported if actual_supported else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    return ClassificationMetrics(
        sample_count=count,
        accuracy=sum(matrix[label][label] for label in VERDICTS) / count,
        precision=precision,
        recall=recall,
        f1=f1,
        false_approval_rate=false_approval / true_non_supported if true_non_supported else 0.0,
        false_rejection_rate=false_rejection / actual_supported if actual_supported else 0.0,
        abstention_coverage=correct_abstentions / count,
        incorrect_abstention_rate=incorrect_abstentions / count,
        confusion_matrix=matrix,
    )


def metric_dict(metrics: ClassificationMetrics) -> dict[str, object]:
    return {
        "sample_count": metrics.sample_count,
        "accuracy": metrics.accuracy,
        "precision": metrics.precision,
        "recall": metrics.recall,
        "f1": metrics.f1,
        "false_approval_rate": metrics.false_approval_rate,
        "false_rejection_rate": metrics.false_rejection_rate,
        "abstention_coverage": metrics.abstention_coverage,
        "incorrect_abstention_rate": metrics.incorrect_abstention_rate,
        "confusion_matrix": metrics.confusion_matrix,
    }
