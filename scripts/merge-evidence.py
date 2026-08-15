#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from vaipex_cross_browser.evidence import merge_evidence


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge Vaipex shard evidence.")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    reports = sorted(arguments.input_dir.glob("shard-*.xml"))
    summary = merge_evidence(reports, arguments.output_dir)
    print(
        f"Merged {summary.shards} shards: tests={summary.tests}, "
        f"failures={summary.failures}, errors={summary.errors}, "
        f"status={summary.status}."
    )
    return 0 if summary.status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
