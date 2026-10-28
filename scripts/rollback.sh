#!/usr/bin/env bash
# Manual rollback to the previously deployed version (stored in .release/previous).
# Usage: scripts/rollback.sh
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .release/previous ] || { echo "No previous release recorded"; exit 1; }
PREV="$(cat .release/previous)"
CUR="$(cat .release/current 2>/dev/null || echo none)"
set -a; . ./.env; set +a
echo ">> Rolling back $CUR -> $PREV"
export APP_TAG="$PREV"
docker compose up -d --no-build
scripts/smoke_test.sh
echo "$CUR" > .release/previous
echo "$PREV" > .release/current
echo ">> Rollback complete: $PREV is live"
