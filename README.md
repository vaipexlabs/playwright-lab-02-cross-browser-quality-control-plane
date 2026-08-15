# Vaipex Cross-Browser Quality Control Plane

An open reference implementation for governing browser, device, and viewport
compatibility through a consistent Playwright and Python test matrix. It helps
teams turn compatibility expectations into repeatable quality signals that run
the same way on a workstation and in continuous integration.

Developed by **Vaipex Labs** for the developer and quality engineering
communities.

![Focus](https://img.shields.io/badge/Focus-Cross--Browser%20Quality-6D42E8)
![Playwright](https://img.shields.io/badge/Playwright-Python-2EAD33?logo=playwright&logoColor=white)
![Browsers](https://img.shields.io/badge/Browsers-Chromium%20%7C%20Firefox%20%7C%20WebKit-2877FF)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

[Project Intent](#project-intent) ·
[Quality Contract](#quality-contract) ·
[Delivery Flow](#delivery-flow) ·
[Architecture](#architecture) ·
[Target Experience](#target-experience) ·
[Delivery Roadmap](#delivery-roadmap) ·
[Repository Structure](#repository-structure)

## Project Intent

A journey that passes in one browser does not prove that customers receive a
consistent experience. Browser engines, viewports, input models, locale, and
network conditions can expose different failures. Running every combination
indiscriminately, however, makes feedback slow and expensive.

This project demonstrates a governed compatibility capability that:

- Declares supported browser and device profiles as versioned configuration.
- Runs the right coverage at pull-request, main-branch, and scheduled stages.
- Reuses business journeys without duplicating browser-specific test code.
- Separates genuine product defects from infrastructure and test instability.
- Preserves browser-specific traces, screenshots, videos, and reports.
- Produces one clear compatibility decision for delivery automation.
- Makes coverage, duration, and failure patterns visible to platform teams.

## Quality Contract

The control plane will enforce five principles:

1. **Explicit support:** every browser and device profile has an owner and
   purpose.
2. **Risk-based coverage:** fast representative checks run before broader
   compatibility suites.
3. **Journey reuse:** tests describe customer outcomes, not browser branches.
4. **Isolated execution:** matrix cells own their context, data, and evidence.
5. **Stable decision:** delivery systems consume one aggregated quality gate.

## Delivery Flow

A change moves from an explicit compatibility policy to isolated execution,
comparable evidence, and a single governed release decision.

![Vaipex cross-browser quality flow](docs/images/vaipex-cross-browser-flow.svg)

## Architecture

Developers and GitHub Actions invoke the same Python control layer. A matrix
orchestrator expands the declared policy into browser and device profiles,
executes reusable journeys against the reference application, and aggregates
the resulting evidence into one quality decision.

![Vaipex cross-browser quality architecture](docs/images/vaipex-cross-browser-architecture.svg)

## Target Experience

The finished implementation will provide one short demonstration:

```bash
./scripts/two-minute-demo.sh
```

It will validate the locked toolchain, execute representative Chromium,
Firefox, WebKit, desktop, and mobile profiles, merge their evidence, and print
the final compatibility decision.

## Compatibility Dimensions

| Dimension | Planned profiles |
| --- | --- |
| Browser engine | Chromium, Firefox, WebKit |
| Desktop viewport | Standard laptop and wide desktop |
| Mobile device | Touch-oriented phone profiles |
| Environment | Local reference application or compatible deployed target |
| Execution stage | Pull request, main branch, and scheduled regression |
| Evidence | HTML, JUnit, trace, screenshot, and video |

The matrix will remain intentionally small. Each profile must detect a distinct
risk or provide a deliberate release signal.

## Delivery Roadmap

- [x] Establish the repository, quality contract, licensing, and project shape.
- [ ] Add the locked Python and Playwright toolchain.
- [ ] Deliver a deterministic responsive reference application.
- [ ] Implement reusable journeys across Chromium, Firefox, and WebKit.
- [ ] Add desktop, mobile, locale, and capability profiles.
- [ ] Introduce risk-based suites, sharding, and merged evidence.
- [ ] Enforce the cross-browser matrix through GitHub Actions.
- [ ] Publish the two-minute demo and operating guidance.

Each milestone is independently reviewable and preserves a usable project
state.

## Toolchain

| Tool | Role |
| --- | --- |
| Python | Automation and orchestration language |
| Playwright for Python | Chromium, Firefox, WebKit, and device emulation |
| Pytest | Fixtures, markers, parametrization, and assertions |
| pytest-xdist | Parallel matrix execution |
| FastAPI | Deterministic responsive reference application |
| Ruff | Python formatting and linting |
| GitHub Actions | Continuous compatibility-gate enforcement |

Dependencies will be declared in `pyproject.toml` and fully pinned before the
first executable milestone.

## Repository Structure

```text
.github/             Continuous quality and dependency automation
docs/images/         Vaipex delivery-flow and architecture illustrations
src/                 Python control plane and reference application
tests/               Fast contracts and reusable browser journeys
scripts/             Supported setup, execution, and demonstration commands
pyproject.toml       Package metadata and tool configuration
```

## Contributing

Community contributions are welcome. Keep compatibility profiles intentional,
journeys browser-agnostic, execution isolated, and evidence actionable.

Licensed under the [Apache License 2.0](LICENSE).
