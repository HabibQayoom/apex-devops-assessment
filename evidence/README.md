# Evidence checklist (replace each item with your real screenshot/log)

- [ ] 01-tests-pass.png: `ruff check .` and `pytest -v` output (local)
- [ ] 02-ci-pass.png: GitHub Actions run, all 3 jobs green
- [ ] 03-ci-fail-blocked.png: run with `simulate_failure` ticked, test fails, build/deploy skipped
- [ ] 04-docker-build.png: `scripts/release.sh v1.0.0`
- [ ] 05-compose-up.png: `scripts/deploy.sh v1.0.0` and `docker compose ps` (healthy)
- [ ] 06-api-calls.png: curl to /health, /ready, POST and GET /operations
- [ ] 07-persistence.png: `docker compose down` then `up`, data still there
- [ ] 08-nonroot.png: `docker compose exec api id` shows uid 10001
- [ ] 09-bad-release-autorollback.png: deploy of `v1.1.0-bad` rolls back
- [ ] 10-manual-rollback.png: `scripts/rollback.sh`
- [ ] 11-db-failure-ready-503.png, 12-logs-error.png, 13-recovery.png
- [ ] 14-metrics.png: /metrics (optional: Prometheus UI and alert rules)
- [ ] 15-trivy-scan.png: scan step from the CI run
