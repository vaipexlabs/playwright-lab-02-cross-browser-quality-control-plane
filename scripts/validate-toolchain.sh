#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"

echo "1/3 Verify the resolved dependency graph"
"${REPOSITORY_ROOT}/.venv/bin/python" -m pip check

echo
echo "2/3 Enforce formatting and lint rules"
"${REPOSITORY_ROOT}/.venv/bin/ruff" format --check "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/ruff" check "${REPOSITORY_ROOT}"

echo
echo "3/3 Verify the package and compatibility contract"
"${REPOSITORY_ROOT}/.venv/bin/pytest" "${REPOSITORY_ROOT}/tests/unit"
"${REPOSITORY_ROOT}/.venv/bin/python" - <<'PY'
from importlib.metadata import version

expected = {
    "playwright": "1.62.0",
    "pytest": "9.1.1",
    "pytest-playwright": "0.9.0",
    "pytest-xdist": "3.8.0",
    "ruff": "0.16.3",
}
for package, expected_version in expected.items():
    actual_version = version(package)
    if actual_version != expected_version:
        raise SystemExit(
            f"{package} version mismatch: expected {expected_version}, found {actual_version}"
        )
    print(f"{package}=={actual_version}")
PY

echo
echo "PASS: the pinned cross-browser toolchain is ready."
