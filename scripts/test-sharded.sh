#!/usr/bin/env bash

set -uo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
SHARD_TOTAL="${VAIPEX_SHARD_TOTAL:-2}"
REPORT_DIRECTORY="${REPOSITORY_ROOT}/reports/shards"
MERGED_DIRECTORY="${REPOSITORY_ROOT}/reports/merged"

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh" || exit 1
if [[ "${VAIPEX_SKIP_BROWSER_INSTALL:-0}" != "1" ]]; then
  "${REPOSITORY_ROOT}/scripts/install-browsers.sh" chromium firefox webkit || exit 1
fi
mkdir -p "${REPORT_DIRECTORY}" "${MERGED_DIRECTORY}"
rm -f \
  "${REPORT_DIRECTORY}"/shard-*.html \
  "${REPORT_DIRECTORY}"/shard-*.log \
  "${REPORT_DIRECTORY}"/shard-*.xml

pids=()
for shard_index in $(seq 1 "${SHARD_TOTAL}"); do
  echo "Starting shard ${shard_index}/${SHARD_TOTAL}"
  VAIPEX_SKIP_BROWSER_INSTALL=1 \
    "${REPOSITORY_ROOT}/scripts/run-shard.sh" "${shard_index}" "${SHARD_TOTAL}" \
    >"${REPORT_DIRECTORY}/shard-${shard_index}.log" 2>&1 &
  pids+=("$!")
done

shard_failure=0
for position in "${!pids[@]}"; do
  shard_index=$((position + 1))
  if wait "${pids[${position}]}"; then
    echo "Shard ${shard_index}/${SHARD_TOTAL} passed."
  else
    echo "Shard ${shard_index}/${SHARD_TOTAL} failed." >&2
    shard_failure=1
  fi
  sed -n '1,220p' "${REPORT_DIRECTORY}/shard-${shard_index}.log"
done

merge_failure=0
"${REPOSITORY_ROOT}/.venv/bin/python" \
  "${REPOSITORY_ROOT}/scripts/merge-evidence.py" \
  --input-dir "${REPORT_DIRECTORY}" \
  --output-dir "${MERGED_DIRECTORY}" || merge_failure=1

echo
echo "Merged evidence:"
echo "  HTML:  ${MERGED_DIRECTORY}/index.html"
echo "  JUnit: ${MERGED_DIRECTORY}/junit.xml"
echo "  JSON:  ${MERGED_DIRECTORY}/summary.json"

if [[ "${shard_failure}" -ne 0 || "${merge_failure}" -ne 0 ]]; then
  exit 1
fi
echo "PASS: every shard and the merged quality decision succeeded."
