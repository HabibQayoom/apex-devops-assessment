"""Static checks that guard security/config hygiene (assessment red flags)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_dockerfile_runs_as_non_root():
    text = (ROOT / "Dockerfile").read_text()
    users = re.findall(r"^USER\s+(\S+)", text, flags=re.MULTILINE)
    assert users, "Dockerfile must set a USER"
    assert users[-1] not in ("root", "0")


def test_compose_has_no_hardcoded_passwords():
    text = (ROOT / "docker-compose.yml").read_text()
    for line in text.splitlines():
        if line.strip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        if "PASSWORD" in key:
            assert value.strip().startswith("${"), f"hard-coded secret? {line.strip()}"


def test_env_file_is_gitignored_and_example_exists():
    assert ".env" in (ROOT / ".gitignore").read_text().splitlines()
    assert (ROOT / ".env.example").exists()


def test_dockerignore_excludes_secrets():
    assert ".env" in (ROOT / ".dockerignore").read_text().splitlines()
