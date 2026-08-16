# Vaipex Cross-Browser Quality Control Plane

An open reference implementation for governing browser, device, locale, and
viewport compatibility through a consistent Playwright and Python quality
matrix. It turns a declared support policy into repeatable release evidence
that behaves the same way on a workstation and in continuous integration.

Developed by **Vaipex Labs** for the developer and quality engineering
communities.

[![Cross-Browser Quality Matrix](https://github.com/vaipexlabs/playwright-lab-02-cross-browser-quality-control-plane/actions/workflows/cross-browser-quality.yaml/badge.svg)](https://github.com/vaipexlabs/playwright-lab-02-cross-browser-quality-control-plane/actions/workflows/cross-browser-quality.yaml)
![Playwright](https://img.shields.io/badge/Playwright-Python-2EAD33?logo=playwright&logoColor=white)
![Browsers](https://img.shields.io/badge/Browsers-Chromium%20%7C%20Firefox%20%7C%20WebKit-2877FF)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

[Capabilities](#capabilities) ·
[How It Works](#how-it-works) ·
[Two-Minute Demo](#two-minute-demo) ·
[Test It Manually](#test-it-manually) ·
[Compatibility Policy](#compatibility-policy) ·
[Control Architecture](#control-architecture) ·
[Continuous Quality Gate](#continuous-quality-gate) ·
[Customize](#customize-the-control-plane) ·
[Operations](#operations)

## Capabilities

| Capability | Implementation |
| --- | --- |
| Browser-engine coverage | The same customer journeys run in Chromium, Firefox, and WebKit |
| Responsive coverage | Versioned desktop and touch-oriented mobile viewport profiles |
| Runtime compatibility | Locale, timezone, touch, pixel-density, and reduced-motion contracts |
| Risk-based execution | Fast smoke checks and a broader regression signal |
| Parallel scale-out | Stable round-robin sharding over fully parameterized test IDs |
| Evidence | HTML, JUnit, logs, traces, screenshots, videos, and JSON decisions |
| Release governance | One merged compatibility decision instead of unrelated matrix results |
| Continuous enforcement | Pull-request, `main`, scheduled, and manually dispatched GitHub Actions runs |
| Reference application | A deterministic responsive experience with no third-party test dependency |
| Developer experience | Locked setup, supported scripts, a two-minute demo, and operating guidance |

## How It Works

![Vaipex cross-browser quality flow](docs/images/vaipex-cross-browser-flow.svg)

The operating principle is:

> Declare the compatibility promise, reuse customer journeys across isolated
> profiles, preserve browser-specific evidence, and publish one release signal.

A developer runs the same supported scripts used by GitHub Actions. The
control plane expands shared journeys across browser engines and compatibility
profiles, isolates every execution, and retains failure evidence. Shard
results are then merged into a decision that delivery automation can consume.

## Two-Minute Demo

### Prerequisites

- Python 3.12
- A macOS or Linux workstation
- Internet access for the one-time dependency and browser installation

Prepare the pinned environment once:

```bash
./scripts/setup.sh
./scripts/install-browsers.sh
```

### Run the demonstration

```bash
./scripts/two-minute-demo.sh
```

The command proves four outcomes:

1. The locked dependencies, formatting rules, and unit contracts are valid.
2. Six core journeys run across three engines in two deterministic shards.
3. Ten checks exercise desktop, mobile, locale, touch, and motion profiles.
4. All sixteen executions become one machine-readable compatibility decision.

Expected final output:

```text
Decision:              PASSED
Browser engines:       3
Compatibility profiles: 5
Total executions:      16
Failures / errors:     0 / 0

PASS: browser engines and compatibility profiles satisfied the contract.
```

Open `reports/merged/index.html` for the consolidated browser report. The
overall demonstration decision is written to `reports/demo/summary.json`.

## Test It Manually

### 1. Explore the reference application

The repository includes **Vaipex Explorer**, a deterministic responsive
planning application built specifically for compatibility automation:

```bash
./scripts/start-app.sh
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and stop it with `Ctrl+C`.
It provides responsive navigation, deterministic catalog search, locale-aware
prices, a client-side itinerary, an accessible booking dialog, stable APIs,
and explicit test controls.

### 2. Run the three-engine journeys

```bash
./scripts/test-cross-browser.sh
```

Two browser-agnostic customer outcomes run in Chromium, Firefox, and WebKit:

- filter the catalog, add an experience, and verify the itinerary;
- build a multi-city plan and receive a deterministic booking confirmation.

The six executions share page objects, configuration, and assertions. Each
engine receives a fresh context, while the application starts and stops
automatically.

### 3. Run the compatibility profiles

```bash
./scripts/test-profiles.sh
```

The five profiles prove their declared browser-context contract before running
a real catalog-to-itinerary outcome.

### 4. Choose the risk signal

Run the fastest representative signal during development:

```bash
./scripts/test-risk-suite.sh smoke
```

Run both core journeys in every engine before release:

```bash
./scripts/test-risk-suite.sh regression
```

### 5. Prove parallel execution and evidence merging

```bash
./scripts/test-sharded.sh
```

The sharding algorithm sorts fully parameterized Pytest node IDs and assigns
them round-robin. Collection order cannot change ownership, every execution
belongs to exactly one shard, and invalid shard coordinates fail before a
browser starts.

Point the core journeys at a compatible deployed target when required:

```bash
VAIPEX_BASE_URL=https://explorer.example.test ./scripts/test-cross-browser.sh
```

## Compatibility Policy

| Profile | Risk represented |
| --- | --- |
| `desktop-standard` | Primary 1440×900 desktop release signal |
| `desktop-compact` | Constrained 1024×768 layout and British English |
| `mobile-touch` | 390×844 viewport, touch input, and 3× pixel density |
| `french-locale` | French formatting and European timezone behavior |
| `reduced-motion` | Operating-system preference for reduced motion |

Core customer journeys run across all three engines. The additional profiles
run in Chromium as representative capability checks. This risk-based design
avoids fifteen mostly redundant engine/profile combinations while retaining a
deliberate signal for every supported dimension.

The policy follows five rules:

1. Every supported profile represents an explicit customer or platform risk.
2. Tests describe customer outcomes and contain no browser-specific branches.
3. Matrix cells own their context, data, and evidence.
4. Fast signals precede broader compatibility coverage.
5. Delivery consumes the merged decision, not an individual test result.

## Control Architecture

![Vaipex cross-browser quality architecture](docs/images/vaipex-cross-browser-architecture.svg)

| Component | Responsibility |
| --- | --- |
| Vaipex Explorer | Provide deterministic responsive behavior and test data |
| Pytest | Compose fixtures, markers, parametrization, and assertions |
| Playwright | Drive Chromium, Firefox, WebKit, and emulated browser contexts |
| Page objects | Keep shared customer journeys independent of browser details |
| Shard selector | Assign stable, non-overlapping test ownership |
| Evidence merger | Produce consolidated HTML, JUnit, and JSON results |
| GitHub Actions | Orchestrate continuous execution and artifact retention |

## Continuous Quality Gate

The workflow under `.github/workflows/cross-browser-quality.yaml` triggers for
pull requests, `main`, weekday schedules, and manual dispatches. It:

1. validates the locked toolchain and fast quality contract;
2. runs two browser shards concurrently with fail-fast disabled;
3. runs the five compatibility profiles on an independent runner;
4. downloads shard artifacts and publishes one merged quality decision.

External actions are pinned to immutable commits. The workflow uses read-only
repository permissions, concurrency control, explicit timeouts, pip caching,
and failure-safe artifact upload. Shard and profile evidence is retained for
seven days; the merged decision is retained for fourteen days.

Configure **Merged quality decision** as the required branch-protection check.

## Evidence

| Evidence | Location |
| --- | --- |
| Final demo decision | `reports/demo/summary.json` |
| Consolidated human report | `reports/merged/index.html` |
| Consolidated machine report | `reports/merged/junit.xml` |
| Per-shard reports and logs | `reports/shards/` |
| Per-profile reports | `reports/profiles/` |
| Failure traces, screenshots, and videos | `artifacts/` |

Generated evidence is intentionally excluded from Git. See the
[operating guide](docs/operations.md) for triage, retention, environment, and
cleanup procedures.

## Customize the Control Plane

Adopters can replace the reference application or individual tools while
preserving the control contract:

- add profiles only when they represent a distinct, owned compatibility risk;
- change smoke and regression markers without duplicating customer journeys;
- change the shard count while retaining deterministic, non-overlapping
  assignment;
- target a deployed application that implements the same accessible UI and
  reset contract;
- publish evidence to another quality platform while retaining human and
  machine-readable decisions;
- replace GitHub Actions with an orchestrator that invokes the same supported
  repository scripts.

Policy changes should update configuration, tests, documentation, and CI
together. Do not hide a browser difference inside conditional test logic.

## Operations

The [operating guide](docs/operations.md) contains supported commands,
evidence locations, failure triage, common problems, policy-change guidance,
and cleanup instructions.

Runtime settings can be changed without editing test code:

| Variable | Purpose |
| --- | --- |
| `VAIPEX_BASE_URL` | Test a compatible deployed environment |
| `VAIPEX_EXPECT_TIMEOUT_MS` | Adjust validated Playwright timeouts |
| `VAIPEX_TRAVELER_NAME` | Override deterministic booking identity |
| `VAIPEX_TRAVELER_EMAIL` | Override deterministic booking email |
| `VAIPEX_SHARD_TOTAL` | Change the local parallel shard count |

## Toolchain

| Tool | Role |
| --- | --- |
| Python 3.12 | Automation and orchestration language |
| Playwright for Python | Browser engines and context emulation |
| Pytest | Fixtures, markers, parametrization, and assertions |
| FastAPI | Deterministic responsive reference application |
| Ruff | Python formatting and linting |
| GitHub Actions | Continuous compatibility-gate enforcement |

Direct dependencies are declared in `pyproject.toml`; the complete transitive
environment is pinned in `requirements.lock`.

## Project Boundaries

This repository demonstrates browser-compatibility governance and release
evidence. It is not a cloud device farm, visual-regression platform,
accessibility certification suite, performance-testing system, or replacement
for production monitoring. Those capabilities can consume the same declared
profiles and evidence boundaries without being hidden inside this project.

## Repository Structure

```text
.github/workflows/  Continuous cross-browser quality gate
docs/               Architecture images and operating guidance
src/                Python control plane and reference application
tests/               Fast contracts and reusable browser journeys
scripts/             Supported setup, execution, and demo commands
pyproject.toml       Package metadata and tool configuration
requirements.lock   Fully resolved dependency versions
```

## Contributing

Community contributions are welcome. Keep profiles intentional, journeys
browser-agnostic, execution isolated, and evidence actionable.

Licensed under the [Apache License 2.0](LICENSE).
