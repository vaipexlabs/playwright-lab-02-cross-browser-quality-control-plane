from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class DemoSummary:
    status: str
    browser_engines: int
    compatibility_profiles: int
    core_executions: int
    profile_executions: int
    total_executions: int
    failures: int
    errors: int


def _junit_totals(report_paths: list[Path]) -> tuple[int, int, int]:
    tests = failures = errors = 0
    for report_path in report_paths:
        root = ET.parse(report_path).getroot()
        suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
        for suite in suites:
            tests += int(suite.get("tests", "0"))
            failures += int(suite.get("failures", "0"))
            errors += int(suite.get("errors", "0"))
    return tests, failures, errors


def summarize_demo(
    core_summary_path: Path,
    profile_report_paths: list[Path],
    output_path: Path,
) -> DemoSummary:
    if not core_summary_path.is_file():
        raise ValueError(f"Core summary not found: {core_summary_path}")
    if len(profile_report_paths) != 5:
        raise ValueError("The demo requires exactly five compatibility reports.")

    core = json.loads(core_summary_path.read_text(encoding="utf-8"))
    profile_tests, profile_failures, profile_errors = _junit_totals(
        sorted(profile_report_paths)
    )
    core_tests = int(core["tests"])
    failures = int(core["failures"]) + profile_failures
    errors = int(core["errors"]) + profile_errors
    contract_complete = (
        core.get("status") == "passed"
        and int(core["shards"]) == 2
        and core_tests == 6
        and profile_tests == 10
    )
    summary = DemoSummary(
        status=(
            "passed"
            if contract_complete and failures == 0 and errors == 0
            else "failed"
        ),
        browser_engines=3,
        compatibility_profiles=len(profile_report_paths),
        core_executions=core_tests,
        profile_executions=profile_tests,
        total_executions=core_tests + profile_tests,
        failures=failures,
        errors=errors,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(summary), indent=2) + "\n",
        encoding="utf-8",
    )
    return summary
