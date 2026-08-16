#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
SHARD_INDEX="${1:-}"
SHARD_TOTAL="${2:-}"
REPORT_DIRECTORY="${REPOSITORY_ROOT}/reports/shards"
ARTIFACT_DIRECTORY="${REPOSITORY_ROOT}/artifacts/shards/shard-${SHARD_INDEX}"

if [[ -z "${SHARD_INDEX}" || -z "${SHARD_TOTAL}" ]]; then
  echo "Usage: ./scripts/run-shard.sh SHARD_INDEX SHARD_TOTAL" >&2
  exit 2
fi

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"
if [[ "${VAIPEX_SKIP_BROWSER_INSTALL:-0}" != "1" ]]; then
  "${REPOSITORY_ROOT}/scripts/install-browsers.sh" chromium firefox webkit
fi
mkdir -p "${REPORT_DIRECTORY}" "${ARTIFACT_DIRECTORY}"

cd "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/pytest" \
  tests/e2e/test_cross_browser_journeys.py \
  -m compatibility \
  --browser chromium \
  --browser firefox \
  --browser webkit \
  --shard-index "${SHARD_INDEX}" \
  --shard-total "${SHARD_TOTAL}" \
  --output "${ARTIFACT_DIRECTORY}" \
  --tracing retain-on-failure \
  --screenshot only-on-failure \
  --video retain-on-failure \
  --html "${REPORT_DIRECTORY}/shard-${SHARD_INDEX}.html" \
  --self-contained-html \
  --junitxml "${REPORT_DIRECTORY}/shard-${SHARD_INDEX}.xml"
