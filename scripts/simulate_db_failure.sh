#!/usr/bin/env bash
# Failure investigation demo: stop the database and watch the API degrade.
# Usage: scripts/simulate_db_failure.sh stop|start
set -euo pipefail
cd "$(dirname "$0")/.."
case "${1:-}" in
  stop)  docker compose stop db; echo "DB stopped. Now follow docs/failure-investigation.md" ;;
  start) docker compose start db; echo "DB started. /ready should recover in a few seconds" ;;
  *) echo "usage: $0 stop|start"; exit 1 ;;
esac
