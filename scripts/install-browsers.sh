#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"

if [[ "$#" -eq 0 ]]; then
  browsers=(chromium firefox webkit)
else
  browsers=("$@")
fi

for browser in "${browsers[@]}"; do
  case "${browser}" in
    chromium | firefox | webkit) ;;
    *)
      echo "Unsupported browser '${browser}'. Choose chromium, firefox, or webkit." >&2
      exit 2
      ;;
  esac
done

echo "Installing Playwright browsers: ${browsers[*]}"
install_arguments=(install "${browsers[@]}")
if [[ "${PLAYWRIGHT_WITH_DEPS:-0}" == "1" ]]; then
  install_arguments=(install --with-deps "${browsers[@]}")
fi
"${REPOSITORY_ROOT}/.venv/bin/playwright" "${install_arguments[@]}"
echo "Requested browsers are ready."
