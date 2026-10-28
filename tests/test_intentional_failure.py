"""Intentional failure used to PROVE the CI gate blocks deployment.

Skipped by default. The CI workflow runs it only when started manually with
'simulate_failure' = true (Actions > CI > Run workflow). See docs/runbook.md.
"""
import os

import pytest


@pytest.mark.skipif(
    os.environ.get("RUN_INTENTIONAL_FAILURE") != "1",
    reason="only runs in the deliberate failure demo",
)
def test_intentional_failure_blocks_deploy():
    assert 1 == 2, "Intentional failure: deployment must be blocked"
