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

## Evidence index (text logs of real command output)

- [01-lint-and-tests.txt](01-lint-and-tests.txt): ruff check passed, pytest 15 passed, 1 skipped
- [02-release-deploy-v1.0.0.txt](02-release-deploy-v1.0.0.txt): release and deploy of v1.0.0, then /health, /ready, POST and GET /operations, /metrics
- [03-persistence-and-nonroot.txt](03-persistence-and-nonroot.txt): docker compose down and up, data persisted, API runs as uid 10001
- [04-bad-release-and-rollback.txt](04-bad-release-and-rollback.txt): v1.1.0-bad failed its smoke test and rolled back automatically, then v1.1.0 deploy and manual rollback
- [05-db-failure-investigation.txt](05-db-failure-investigation.txt): DB stopped, /health 200, /ready 503, app_db_up 0, then recovery
- [06-ci-green-run.txt](06-ci-green-run.txt): green CI run with test, build and scan, and deploy jobs passing
- [07-ci-simulated-failure.txt](07-ci-simulated-failure.txt): simulate_failure=true run, tests failed, build and deploy skipped
- [08-ci-failed-runs-before-fix.txt](08-ci-failed-runs-before-fix.txt): two earlier failed CI runs (trivy-action tag not found, then setup-trivy tag not found) before the fix

## CI troubleshooting

Both earlier CI failures were caused by GitHub Action version tags that no longer resolve:
`aquasecurity/trivy-action@0.28.0` (the tag is `v0.28.0`), and then `aquasecurity/setup-trivy@v0.2.1`,
which trivy-action v0.28.0 calls internally. Both were fixed by updating trivy-action to `v0.36.0`.
