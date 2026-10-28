#!/usr/bin/env bash
# Wait until /ready returns 200, then check core endpoints.
set -euo pipefail
BASE="${BASE_URL:-http://localhost:8000}"
for i in $(seq 1 30); do
  if curl -fsS "$BASE/ready" >/dev/null 2>&1; then
    curl -fsS "$BASE/health" >/dev/null
    curl -fsS "$BASE/version"; echo
    echo "SMOKE TEST PASSED"
    exit 0
  fi
  sleep 2
done
echo "SMOKE TEST FAILED: /ready did not return 200" >&2
exit 1
