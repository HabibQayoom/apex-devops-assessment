#!/usr/bin/env bash
# Deploy a specific image version with Docker Compose.
# Records current/previous versions in .release/ and auto-rolls back if the smoke test fails.
# Usage: scripts/deploy.sh v1.0.0
set -euo pipefail
cd "$(dirname "$0")/.."
VERSION="${1:?usage: scripts/deploy.sh <version>}"
mkdir -p .release
[ -f .env ] || { echo "Missing .env (cp .env.example .env)"; exit 1; }
set -a; . ./.env; set +a

CURRENT=""
[ -f .release/current ] && CURRENT="$(cat .release/current)"

echo ">> Deploying $VERSION (current: ${CURRENT:-none})"
export APP_TAG="$VERSION"
docker compose up -d --no-build

if scripts/smoke_test.sh; then
  [ -n "$CURRENT" ] && [ "$CURRENT" != "$VERSION" ] && echo "$CURRENT" > .release/previous
  echo "$VERSION" > .release/current
  echo ">> Deploy OK: $VERSION is live"
else
  echo ">> Deploy FAILED for $VERSION" >&2
  if [ -n "$CURRENT" ] && [ "$CURRENT" != "$VERSION" ]; then
    echo ">> Automatic rollback to $CURRENT" >&2
    export APP_TAG="$CURRENT"
    docker compose up -d --no-build
    scripts/smoke_test.sh && echo ">> Rolled back to $CURRENT" >&2
  fi
  exit 1
fi
