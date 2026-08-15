#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
VIRTUAL_ENVIRONMENT="${REPOSITORY_ROOT}/.venv"
INSTALLED_LOCK="${VIRTUAL_ENVIRONMENT}/.requirements.lock"

if [[ ! -x "${VIRTUAL_ENVIRONMENT}/bin/python" ]] || \
  [[ ! -f "${INSTALLED_LOCK}" ]] || \
  ! cmp -s "${REPOSITORY_ROOT}/requirements.lock" "${INSTALLED_LOCK}"; then
  echo "The local toolchain is missing or out of date; reconciling it now."
  "${REPOSITORY_ROOT}/scripts/setup.sh"
fi
