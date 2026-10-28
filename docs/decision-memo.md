# Decision memo

| Decision | Reason | Trade-off |
| --- | --- | --- |
| FastAPI + SQLAlchemy | Small, readable, built-in validation | Not the fastest option, but simple |
| Postgres in Compose with named volume | Realistic dependency with persistence | Single node, no HA |
| Liveness vs readiness split | `/health` shows the process, `/ready` checks the DB | Slightly more code |
| Versioned tags, no `latest` | Deterministic deploy and rollback | Need a version per release |
| Shell scripts for release/rollback | Easy to read, run and explain | Less portable than a tool like Helm |
| Auto-rollback on failed smoke test | Fast recovery, no manual step | Only covers startup failures |
| Simulated bad release flag | Safe, repeatable rollback demo | Test-only code path, documented |
| Intentional failure behind a manual flag | Proves the gate without leaving CI red | Needs a manual workflow run |
| Trivy fails only on fixable CRITICAL | Avoids noisy blocks | Lower severities need review |
| Prometheus as optional profile | Metrics demo without extra weight by default | Alerts are a proposal only |

## Assumptions
Local Docker target, synthetic data, no cloud spend, GitHub Actions available.

## With more time
TLS and auth, DB migrations (Alembic), Alertmanager, image signing, Dependabot,
integration tests against real Postgres in CI, deploy to a cloud VM.
