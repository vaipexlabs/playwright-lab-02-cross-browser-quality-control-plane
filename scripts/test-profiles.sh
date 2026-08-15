#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
REPORT_DIRECTORY="${REPOSITORY_ROOT}/reports/profiles"
ARTIFACT_DIRECTORY="${REPOSITORY_ROOT}/artifacts/profiles"
PROFILES=(
  desktop-standard
  desktop-compact
  mobile-touch
  french-locale
  reduced-motion
)

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"
"${REPOSITORY_ROOT}/scripts/install-browsers.sh" chromium
mkdir -p "${REPORT_DIRECTORY}" "${ARTIFACT_DIRECTORY}"

cd "${REPOSITORY_ROOT}"
for profile in "${PROFILES[@]}"; do
  echo
  echo "Running compatibility profile: ${profile}"
  "${REPOSITORY_ROOT}/.venv/bin/pytest" \
    tests/e2e/test_profile_journeys.py \
    --browser chromium \
    --compatibility-profile "${profile}" \
    --output "${ARTIFACT_DIRECTORY}/${profile}" \
    --tracing retain-on-failure \
    --screenshot only-on-failure \
    --video retain-on-failure \
    --html "${REPORT_DIRECTORY}/${profile}.html" \
    --self-contained-html \
    --junitxml "${REPORT_DIRECTORY}/${profile}.xml" \
    -q
done

echo
echo "PASS: all five compatibility profiles succeeded."
echo "Reports: ${REPORT_DIRECTORY}"
echo "Failure artifacts: ${ARTIFACT_DIRECTORY}"
