# Runtime Validation Record

## Environment

- Python installed through WinGet: 3.12.10
- Project interpreter: `.venv/Scripts/python.exe`
- Test dependencies installed from `backend/requirements.txt`
- Node.js: 24.19.0
- npm: 11.17.0

## Evaluation validation

Executed:

```powershell
.venv\Scripts\python.exe -m pytest backend/tests/test_evaluation.py -q
.venv\Scripts\python.exe -m pytest backend/tests -q
```

Results:

- Evaluation tests: 4 passed
- Complete backend suite: 44 passed
- One third-party deprecation warning from Starlette/httpx compatibility

Runtime API check:

```text
POST /api/evaluation/run -> 200
status: NOT_YET_MEASURED
sample_count: 0
```

This is the correct result because the benchmark contains no manually checked records. No evaluation score is claimed.
