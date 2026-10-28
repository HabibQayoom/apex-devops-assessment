#!/usr/bin/env bash
# Build a versioned image.  Usage: scripts/release.sh v1.0.0 [--bad]
# --bad bakes SIMULATE_BAD_RELEASE=true into the image (used ONLY to demo auto-rollback).
set -euo pipefail
VERSION="${1:?usage: scripts/release.sh <version> [--bad]}"
BAD=false
[ "${2:-}" = "--bad" ] && BAD=true
IMAGE="${APP_IMAGE:-apex-ops-api}"
docker build \
  --build-arg APP_VERSION="$VERSION" \
  --build-arg SIMULATE_BAD_RELEASE="$BAD" \
  -t "$IMAGE:$VERSION" .
echo "Built $IMAGE:$VERSION (bad=$BAD)"
