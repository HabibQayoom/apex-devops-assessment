# Runbook

## 1. Deploy
```bash
cp .env.example .env && edit POSTGRES_PASSWORD
scripts/release.sh v1.0.0
scripts/deploy.sh v1.0.0
```
Success looks like `SMOKE TEST PASSED` and `Deploy OK`. Verify: `docker compose ps` shows
`db` and `api` as healthy.

## 2. Release a new version
```bash
scripts/release.sh v1.1.0
scripts/deploy.sh v1.1.0      # previous version is saved in .release/previous
```

## 3. Rollback
Automatic: if the smoke test fails, `deploy.sh` redeploys the previous version.
Manual: `scripts/rollback.sh` (redeploys `.release/previous`, then swaps the records).
Demonstrate both:
```bash
scripts/release.sh v1.0.0 && scripts/deploy.sh v1.0.0
scripts/release.sh v1.1.0-bad --bad       # simulated bad release (readiness returns 503)
scripts/deploy.sh v1.1.0-bad              # smoke test fails -> automatic rollback to v1.0.0
curl localhost:8000/version               # shows v1.0.0
scripts/release.sh v1.1.0 && scripts/deploy.sh v1.1.0
scripts/rollback.sh                       # manual rollback to v1.0.0
```
Database rollback note: this app only adds rows and has no schema migrations. With migrations,
use backward-compatible (expand/contract) changes so the old image still works.

## 4. Incident response
1. Check: `curl -i localhost:8000/ready` (503 = dependency or bad release).
2. Check: `docker compose ps` and `docker compose logs --tail=100 api db`.
3. Look at JSON logs: `docker compose logs api | grep '"level": "ERROR"'`.
4. Decide: dependency down -> restore it; bad release -> `scripts/rollback.sh`.
5. Verify: `scripts/smoke_test.sh`.
6. Record what happened, impact, cause and fix (short post-incident note).

## 4b. Severity guide
Sev1: API down for all users, roll back first, investigate after. Sev2: degraded
(errors/latency). Sev3: cosmetic or single endpoint.

## 5. Troubleshooting
| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `set POSTGRES_PASSWORD in .env` | Missing `.env` | `cp .env.example .env` |
| `/ready` 503, "database unavailable" | DB stopped or unhealthy | `docker compose start db` |
| `/ready` 503, "simulated bad release" | Bad image deployed | `scripts/rollback.sh` |
| Port 8000 in use | Another process | Stop it or change the port mapping |
| API restarts in a loop | DB not ready or wrong creds | `docker compose logs api db` |
| CI blocked at `test` | Failing test | Read the pytest output, fix, push |
