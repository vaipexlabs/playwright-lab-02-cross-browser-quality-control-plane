#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
SUITE="${1:-smoke}"
REPORT_DIRECTORY="${REPOSITORY_ROOT}/reports/risk"
ARTIFACT_DIRECTORY="${REPOSITORY_ROOT}/artifacts/risk/${SUITE}"

case "${SUITE}" in
  smoke) marker="smoke" ;;
  regression) marker="smoke or regression" ;;
  *)
    echo "Usage: ./scripts/test-risk-suite.sh [smoke|regression]" >&2
    exit 2
    ;;
esac

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"
"${REPOSITORY_ROOT}/scripts/install-browsers.sh" chromium firefox webkit
mkdir -p "${REPORT_DIRECTORY}" "${ARTIFACT_DIRECTORY}"

cd "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/pytest" \
  tests/e2e/test_cross_browser_journeys.py \
  -m "${marker}" \
  --browser chromium \
  --browser firefox \
  --browser webkit \
  --output "${ARTIFACT_DIRECTORY}" \
  --tracing retain-on-failure \
  --screenshot only-on-failure \
  --video retain-on-failure \
  --html "${REPORT_DIRECTORY}/${SUITE}.html" \
  --self-contained-html \
  --junitxml "${REPORT_DIRECTORY}/${SUITE}.xml"
