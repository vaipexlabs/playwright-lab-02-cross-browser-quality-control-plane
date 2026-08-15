from __future__ import annotations

import copy
import json
import xml.etree.ElementTree as ET
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from html import escape
from pathlib import Path


@dataclass(frozen=True)
class EvidenceSummary:
    status: str
    shards: int
    tests: int
    failures: int
    errors: int
    skipped: int
    duration_seconds: float


def _suites(root: ET.Element) -> list[ET.Element]:
    return [root] if root.tag == "testsuite" else list(root.findall("testsuite"))


def merge_evidence(
    report_paths: Iterable[Path],
    output_directory: Path,
) -> EvidenceSummary:
    paths = sorted(report_paths)
    if not paths:
        raise ValueError("At least one JUnit report is required.")

    output_directory.mkdir(parents=True, exist_ok=True)
    merged_root = ET.Element("testsuites", {"name": "Vaipex sharded browser quality"})
    rows: list[dict[str, str | int | float]] = []
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    duration = 0.0

    for path in paths:
        report_root = ET.parse(path).getroot()
        path_totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
        path_duration = 0.0
        for suite in _suites(report_root):
            merged_root.append(copy.deepcopy(suite))
            for field in path_totals:
                value = int(suite.get(field, "0"))
                path_totals[field] += value
                totals[field] += value
            suite_duration = float(suite.get("time", "0"))
            path_duration += suite_duration
            duration += suite_duration
        rows.append(
            {
                "name": path.stem,
                **path_totals,
                "duration": round(path_duration, 3),
            }
        )

    status = "passed" if totals["failures"] + totals["errors"] == 0 else "failed"
    summary = EvidenceSummary(
        status=status,
        shards=len(paths),
        tests=totals["tests"],
        failures=totals["failures"],
        errors=totals["errors"],
        skipped=totals["skipped"],
        duration_seconds=round(duration, 3),
    )
    merged_root.attrib.update(
        {
            "tests": str(summary.tests),
            "failures": str(summary.failures),
            "errors": str(summary.errors),
            "skipped": str(summary.skipped),
            "time": str(summary.duration_seconds),
        }
    )
    ET.indent(merged_root)
    ET.ElementTree(merged_root).write(
        output_directory / "junit.xml",
        encoding="utf-8",
        xml_declaration=True,
    )
    (output_directory / "summary.json").write_text(
        json.dumps(asdict(summary), indent=2) + "\n",
        encoding="utf-8",
    )
    _write_html_summary(output_directory / "index.html", summary, rows)
    return summary


def _write_html_summary(
    path: Path,
    summary: EvidenceSummary,
    rows: list[dict[str, str | int | float]],
) -> None:
    row_markup = "\n".join(
        "<tr>"
        f'<td><a href="../shards/{escape(str(row["name"]))}.html">'
        f"{escape(str(row['name']))}</a></td>"
        f"<td>{row['tests']}</td><td>{row['failures']}</td>"
        f"<td>{row['errors']}</td><td>{row['duration']}s</td>"
        "</tr>"
        for row in rows
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Vaipex Sharded Browser Quality</title>
  <style>
    body{{font:16px system-ui;margin:0;color:#07164f;background:#f5f7fc}}
    main{{max-width:1000px;margin:60px auto;padding:0 24px}}
    h1{{font-size:42px;margin-bottom:8px}}p{{color:#53617f}}
    .status{{display:inline-block;padding:8px 12px;border-radius:999px;
      color:white;background:#129579;font-weight:700}}
    .metrics{{display:grid;grid-template-columns:repeat(4,1fr);
      gap:16px;margin:32px 0}}
    .metric,table{{background:white;border:1px solid #dce3f0;
      border-radius:14px;box-shadow:0 12px 30px #07164f12}}
    .metric{{padding:22px}}.metric strong{{display:block;font-size:32px}}
    table{{width:100%;border-collapse:collapse;overflow:hidden}}
    th,td{{padding:16px;text-align:left;border-bottom:1px solid #dce3f0}}
    a{{color:#4d32c6}}
  </style>
</head>
<body><main>
  <p>VAIPEX LABS</p><h1>Sharded browser quality</h1>
  <span class="status">{escape(summary.status.upper())}</span>
  <div class="metrics">
    <div class="metric"><strong>{summary.tests}</strong>tests</div>
    <div class="metric"><strong>{summary.shards}</strong>shards</div>
    <div class="metric"><strong>{summary.failures}</strong>failures</div>
    <div class="metric"><strong>{summary.duration_seconds}s</strong>
      combined duration</div>
  </div>
  <table><thead><tr><th>Shard</th><th>Tests</th><th>Failures</th><th>Errors</th><th>Duration</th></tr></thead>
  <tbody>{row_markup}</tbody></table>
</main></body></html>
"""
    path.write_text(html, encoding="utf-8")
