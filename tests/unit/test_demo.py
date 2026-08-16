import json
from pathlib import Path

from vaipex_cross_browser.demo import summarize_demo


def write_profile_report(path: Path, tests: int = 2, failures: int = 0) -> None:
    path.write_text(
        f'<testsuites><testsuite tests="{tests}" failures="{failures}" '
        'errors="0" skipped="0" time="1.0" /></testsuites>',
        encoding="utf-8",
    )


def build_demo_inputs(tmp_path: Path) -> tuple[Path, list[Path]]:
    core_summary = tmp_path / "core.json"
    core_summary.write_text(
        json.dumps(
            {
                "status": "passed",
                "shards": 2,
                "tests": 6,
                "failures": 0,
                "errors": 0,
            }
        ),
        encoding="utf-8",
    )
    profiles = [tmp_path / f"profile-{index}.xml" for index in range(5)]
    for profile in profiles:
        write_profile_report(profile)
    return core_summary, profiles


def test_demo_publishes_one_complete_compatibility_decision(tmp_path: Path) -> None:
    core_summary, profiles = build_demo_inputs(tmp_path)
    output = tmp_path / "demo" / "summary.json"

    summary = summarize_demo(core_summary, profiles, output)

    assert summary.status == "passed"
    assert summary.browser_engines == 3
    assert summary.compatibility_profiles == 5
    assert summary.total_executions == 16
    assert json.loads(output.read_text(encoding="utf-8"))["status"] == "passed"


def test_demo_preserves_a_profile_failure(tmp_path: Path) -> None:
    core_summary, profiles = build_demo_inputs(tmp_path)
    write_profile_report(profiles[0], failures=1)

    summary = summarize_demo(core_summary, profiles, tmp_path / "summary.json")

    assert summary.status == "failed"
    assert summary.failures == 1
