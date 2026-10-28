"""Configuration is read from environment variables only (12-factor). No secrets in code."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str
    app_version: str
    log_level: str
    simulate_bad_release: bool


def get_settings() -> Settings:
    return Settings(
        database_url=os.environ.get("DATABASE_URL", "sqlite:///./local.db"),
        app_version=os.environ.get("APP_VERSION", "dev"),
        log_level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        # Used ONLY to demonstrate an automatic rollback (see docs/runbook.md).
        simulate_bad_release=os.environ.get("SIMULATE_BAD_RELEASE", "false").lower() == "true",
    )
