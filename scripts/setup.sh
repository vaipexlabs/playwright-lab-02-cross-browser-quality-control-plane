#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
VIRTUAL_ENVIRONMENT="${REPOSITORY_ROOT}/.venv"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3.12 is required but python3 was not found." >&2
  exit 1
fi

python_version="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "${python_version}" != "3.12" ]]; then
  echo "Python 3.12 is required; found ${python_version}." >&2
  exit 1
fi

if [[ ! -x "${VIRTUAL_ENVIRONMENT}/bin/python" ]]; then
  echo "Creating Python virtual environment..."
  python3 -m venv "${VIRTUAL_ENVIRONMENT}"
fi

virtual_environment_version="$(
  "${VIRTUAL_ENVIRONMENT}/bin/python" -c \
    'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")'
)"
if [[ "${virtual_environment_version}" != "3.12" ]]; then
  echo "The existing .venv uses Python ${virtual_environment_version}; Python 3.12 is required." >&2
  echo "Remove .venv and rerun ./scripts/setup.sh." >&2
  exit 1
fi

echo "Installing the pinned project toolchain..."
"${VIRTUAL_ENVIRONMENT}/bin/python" -m pip install --quiet --upgrade "pip==26.2.1"
"${VIRTUAL_ENVIRONMENT}/bin/python" -m pip install --quiet \
  --requirement "${REPOSITORY_ROOT}/requirements.lock"
"${VIRTUAL_ENVIRONMENT}/bin/python" -m pip install --quiet \
  --no-deps \
  --no-build-isolation \
  --editable "${REPOSITORY_ROOT}"
cp "${REPOSITORY_ROOT}/requirements.lock" \
  "${VIRTUAL_ENVIRONMENT}/.requirements.lock"

echo "Toolchain ready: ${VIRTUAL_ENVIRONMENT}"
