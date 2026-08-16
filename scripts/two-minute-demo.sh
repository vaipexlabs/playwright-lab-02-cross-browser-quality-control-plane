#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
DEMO_DIRECTORY="${REPOSITORY_ROOT}/reports/demo"

run_step() {
  local number="$1"
  local label="$2"
  local log_path="$3"
  shift 3

  echo "${number}/4 ${label}"
  if "$@" >"${log_path}" 2>&1; then
    echo "    PASS"
  else
    echo "    FAIL — recent output follows" >&2
    tail -n 80 "${log_path}" >&2
    exit 1
  fi
  echo
}

mkdir -p "${DEMO_DIRECTORY}"

echo "Vaipex Cross-Browser Quality Control Plane"
echo "==========================================="
echo

run_step \
  1 \
  "Validate the locked toolchain and quality contract" \
  "${DEMO_DIRECTORY}/01-quality-contract.log" \
  "${REPOSITORY_ROOT}/scripts/validate-toolchain.sh"

run_step \
  2 \
  "Run six Chromium, Firefox, and WebKit executions in two shards" \
  "${DEMO_DIRECTORY}/02-browser-shards.log" \
  env VAIPEX_SKIP_BROWSER_INSTALL=1 \
  "${REPOSITORY_ROOT}/scripts/test-sharded.sh"

run_step \
  3 \
  "Run ten desktop, mobile, locale, touch, and motion checks" \
  "${DEMO_DIRECTORY}/03-compatibility-profiles.log" \
  env VAIPEX_SKIP_BROWSER_INSTALL=1 \
  "${REPOSITORY_ROOT}/scripts/test-profiles.sh"

echo "4/4 Publish one compatibility decision"
"${REPOSITORY_ROOT}/.venv/bin/python" \
  "${REPOSITORY_ROOT}/scripts/summarize-demo.py" \
  --core-summary "${REPOSITORY_ROOT}/reports/merged/summary.json" \
  --profiles-dir "${REPOSITORY_ROOT}/reports/profiles" \
  --output "${DEMO_DIRECTORY}/summary.json"

echo
echo "PASS: browser engines and compatibility profiles satisfied the contract."
echo "Merged HTML: ${REPOSITORY_ROOT}/reports/merged/index.html"
echo "Demo summary: ${DEMO_DIRECTORY}/summary.json"
