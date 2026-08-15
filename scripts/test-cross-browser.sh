#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
REPORT_DIRECTORY="${REPOSITORY_ROOT}/reports"
ARTIFACT_DIRECTORY="${REPOSITORY_ROOT}/artifacts/playwright"

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"
"${REPOSITORY_ROOT}/scripts/install-browsers.sh" chromium firefox webkit
mkdir -p "${REPORT_DIRECTORY}" "${ARTIFACT_DIRECTORY}"

echo "Running shared journeys across Chromium, Firefox, and WebKit..."
cd "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/pytest" \
  tests/e2e \
  -m compatibility \
  --browser chromium \
  --browser firefox \
  --browser webkit \
  --output "${ARTIFACT_DIRECTORY}" \
  --tracing retain-on-failure \
  --screenshot only-on-failure \
  --video retain-on-failure \
  --html "${REPORT_DIRECTORY}/cross-browser.html" \
  --self-contained-html \
  --junitxml "${REPORT_DIRECTORY}/cross-browser.xml"

echo
echo "Reports:"
echo "  HTML:  ${REPORT_DIRECTORY}/cross-browser.html"
echo "  JUnit: ${REPORT_DIRECTORY}/cross-browser.xml"
echo "Failure artifacts: ${ARTIFACT_DIRECTORY}"
