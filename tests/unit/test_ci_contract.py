import re
from pathlib import Path

WORKFLOW = Path(".github/workflows/cross-browser-quality.yaml")


def test_ci_runs_for_change_main_schedule_and_manual_events() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "pull_request:" in workflow
    assert "push:" in workflow
    assert "schedule:" in workflow
    assert "workflow_dispatch:" in workflow


def test_ci_preserves_least_privilege_and_immutable_actions() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    action_references = re.findall(r"uses: [^@\n]+@([^\s#]+)", workflow)

    assert "permissions:\n  contents: read" in workflow
    assert action_references
    assert all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in action_references)


def test_ci_enforces_two_shards_profiles_and_merged_evidence() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    assert "shard: [1, 2]" in workflow
    assert "fail-fast: false" in workflow
    assert "./scripts/run-shard.sh" in workflow
    assert "./scripts/test-profiles.sh" in workflow
    assert "scripts/merge-evidence.py" in workflow
    assert "merged-quality-decision" in workflow
