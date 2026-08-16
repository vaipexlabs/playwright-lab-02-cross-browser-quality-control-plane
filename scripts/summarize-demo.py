#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from vaipex_cross_browser.demo import summarize_demo


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize the Vaipex demo.")
    parser.add_argument("--core-summary", type=Path, required=True)
    parser.add_argument("--profiles-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    summary = summarize_demo(
        arguments.core_summary,
        sorted(arguments.profiles_dir.glob("*.xml")),
        arguments.output,
    )
    print(f"Decision:              {summary.status.upper()}")
    print(f"Browser engines:       {summary.browser_engines}")
    print(f"Compatibility profiles:{summary.compatibility_profiles:>2}")
    print(f"Total executions:      {summary.total_executions}")
    print(f"Failures / errors:     {summary.failures} / {summary.errors}")
    return 0 if summary.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
