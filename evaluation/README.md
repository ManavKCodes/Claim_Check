# Evaluation Workspace

Runtime evaluation code lives under `backend/app/evaluation` so it can be used by the API. This directory marks the project-level evaluation boundary for benchmark manifests, baseline reports, and future measured outputs.

Do not commit fabricated scores. Evaluation output must identify the benchmark version, split strategy, sample count, baseline/system name, and metric values. Empty or incomplete benchmarks must report `NOT_YET_MEASURED`.
