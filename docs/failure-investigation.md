# Failure investigation: database outage

**Scenario:** Postgres stops while the API keeps running.

## Reproduce
```bash
scripts/deploy.sh v1.0.0
scripts/simulate_db_failure.sh stop
curl -i localhost:8000/health      # still 200: process alive (liveness)
curl -i localhost:8000/ready       # 503 {"reason":"database unavailable"}
```

## Investigate (what to look at, in order)
1. `docker compose ps`: `db` is exited, `api` still up.
2. `docker compose logs --tail=50 api`: JSON ERROR lines with `"error": "db_unavailable"`.
3. `curl localhost:8000/metrics | grep app_db_up`: `app_db_up 0`.
4. Metrics show `http_requests_total{status="500"}` or `503` rising on `/operations`.

## Root cause and fix
Database container stopped. Fix: `scripts/simulate_db_failure.sh start`. Verify `/ready`
returns 200 and `app_db_up 1`. Data is intact because it lives on the `pgdata` volume.

## What would alert us
`DatabaseUnavailable` (`app_db_up == 0` for 1m) in `monitoring/alerts.yml`.

## Evidence to capture (replace with your real outputs)
Screenshots: `docker compose ps`, the 503 response, the ERROR log lines, `app_db_up 0`,
and the recovery. Save them in `evidence/`.

## Improvements with more time
Add a DB connection-failure counter, readiness caching, and an Alertmanager route to chat.
