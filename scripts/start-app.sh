#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"

export PYTHONPATH="${REPOSITORY_ROOT}/src"
export VAIPEX_TEST_MODE="${VAIPEX_TEST_MODE:-1}"

echo "Starting Vaipex Explorer at http://127.0.0.1:${PORT:-8000}"
exec "${REPOSITORY_ROOT}/.venv/bin/uvicorn" vaipex_cross_browser.app:app \
  --host 127.0.0.1 \
  --port "${PORT:-8000}"
