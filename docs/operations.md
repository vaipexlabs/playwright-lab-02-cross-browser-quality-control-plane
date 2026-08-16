# Operating Guide

## Supported Entry Points

| Intent | Command |
| --- | --- |
| Validate dependencies, formatting, and unit contracts | `./scripts/validate-toolchain.sh` |
| Run the fast release signal | `./scripts/test-risk-suite.sh smoke` |
| Run all core journeys in three browser engines | `./scripts/test-cross-browser.sh` |
| Run the five compatibility profiles | `./scripts/test-profiles.sh` |
| Run and merge two parallel browser shards | `./scripts/test-sharded.sh` |
| Demonstrate the complete local quality decision | `./scripts/two-minute-demo.sh` |

These scripts are the supported interface. GitHub Actions invokes the same
commands so local and continuous-integration behavior do not drift.

## Evidence Map

| Evidence | Location | Consumer |
| --- | --- | --- |
| Final demo decision | `reports/demo/summary.json` | Developer or release automation |
| Consolidated browser report | `reports/merged/index.html` | Human reviewer |
| Consolidated JUnit | `reports/merged/junit.xml` | CI and quality systems |
| Per-shard HTML, XML, and logs | `reports/shards/` | Failure isolation |
| Per-profile HTML and XML | `reports/profiles/` | Compatibility diagnosis |
| Failure traces, screenshots, and videos | `artifacts/` | Browser-level debugging |

Reports are local generated evidence and are intentionally excluded from Git.
GitHub Actions retains shard and profile artifacts for seven days and the
merged decision for fourteen days.

## Failure Triage

1. Read the failed step and identify the browser engine or profile.
2. Open its HTML report under `reports/shards/` or `reports/profiles/`.
3. Inspect the corresponding trace, screenshot, or video under `artifacts/`.
4. Reproduce only the affected signal with `pytest` and the recorded browser or
   `--compatibility-profile` value.
5. Classify the result as a product defect, automation defect, or execution
   infrastructure failure before retrying it.

Do not make blind retries the release policy. A retry can provide diagnostic
evidence, but the original failure remains part of the engineering signal.

## Common Problems

### A browser executable is missing

Reconcile the pinned browser builds:

```bash
./scripts/install-browsers.sh
```

On Linux, browser operating-system dependencies may also be required:

```bash
PLAYWRIGHT_WITH_DEPS=1 ./scripts/install-browsers.sh
```

### Port 8000 is already in use

The Pytest application fixture selects an available port automatically. Only
the manual application command defaults to port 8000. Choose another port:

```bash
PORT=8001 ./scripts/start-app.sh
```

### A deployed environment should be tested

Point the shared journeys at a compatible target:

```bash
VAIPEX_BASE_URL=https://explorer.example.test ./scripts/test-cross-browser.sh
```

The target must implement the same accessible UI and deterministic reset
contract as Vaipex Explorer.

## Policy Changes

Treat additions to the browser matrix as product decisions. Every profile
should represent a distinct customer or platform risk, have an owner, and
produce an actionable failure. Update the configuration, tests, README, and CI
contract together.

Use **Merged quality decision** as the required GitHub branch-protection check.
This prevents delivery from consuming an individual matrix cell as if it were
the complete compatibility decision.

## Cleanup

Remove generated evidence without touching source or the virtual environment:

```bash
rm -rf artifacts reports
```

Remove the reproducible Python environment as well when a full local reset is
needed:

```bash
rm -rf .venv artifacts reports
```

Run `./scripts/setup.sh` and `./scripts/install-browsers.sh` to restore the
toolchain afterward.
