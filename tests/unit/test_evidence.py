import json
from pathlib import Path

import pytest

from vaipex_cross_browser.evidence import merge_evidence


def write_report(
    path: Path,
    *,
    tests: int,
    failures: int = 0,
    errors: int = 0,
    duration: float = 1.0,
) -> None:
    path.write_text(
        f'<testsuites><testsuite name="{path.stem}" tests="{tests}" '
        f'failures="{failures}" errors="{errors}" skipped="0" '
        f'time="{duration}"></testsuite></testsuites>',
        encoding="utf-8",
    )


def test_reports_are_merged_into_human_and_machine_evidence(tmp_path: Path) -> None:
    reports = tmp_path / "shards"
    output = tmp_path / "merged"
    reports.mkdir()
    write_report(reports / "shard-1.xml", tests=3, duration=2.5)
    write_report(reports / "shard-2.xml", tests=3, duration=2.0)

    summary = merge_evidence(reports.glob("*.xml"), output)

    assert summary.status == "passed"
    assert summary.shards == 2
    assert summary.tests == 6
    assert summary.duration_seconds == 4.5
    assert json.loads((output / "summary.json").read_text())["tests"] == 6
    assert (output / "junit.xml").read_text().count("<testsuite ") == 2
    assert "Sharded browser quality" in (output / "index.html").read_text()


def test_failure_is_preserved_in_merged_decision(tmp_path: Path) -> None:
    report = tmp_path / "failed.xml"
    write_report(report, tests=2, failures=1)

    summary = merge_evidence([report], tmp_path / "merged")

    assert summary.status == "failed"
    assert summary.failures == 1


def test_merge_rejects_empty_report_set(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="At least one JUnit report"):
        merge_evidence([], tmp_path / "merged")
