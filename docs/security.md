# Security, secrets and least privilege

## Secrets
- No secrets in the repo: `.env` is git-ignored; `.env.example` has placeholders only.
- Compose requires `POSTGRES_PASSWORD` (`${POSTGRES_PASSWORD:?}`) so it cannot silently run
  with a default.
- A test fails the build if a password is hard-coded in `docker-compose.yml`.
- CI generates a random throwaway password for its smoke deployment.
- Production path: a secret manager (see cloud-path.md), never env files in git.

## Least privilege
- Container runs as non-root user (uid 10001), enforced by a test.
- `read_only: true` root filesystem, `tmpfs` for `/tmp`, `cap_drop: ALL`,
  `no-new-privileges`.
- Database is not published to the host; only the API port 8000 is.
- Workflow `permissions: contents: read` (no write scopes needed).
- Slim base image, multi-stage build (no build tools in the runtime image).

## Scanning
- `pip-audit` on dependencies in CI.
- Trivy image scan in CI (fails on fixable CRITICAL findings).
- Pinned dependency versions; recommended: Dependabot for updates.

## Known gaps (honest trade-offs)
No TLS or auth on the API (demo scope), `postgres` runs with a local password, no image
signing. Next steps: reverse proxy with TLS, JWT/API keys, cosign signing.
