from __future__ import annotations

import pytest
from playwright.sync_api import Page

from tests.config import AutomationSettings, Traveler
from vaipex_cross_browser.profiles import (
    DEFAULT_PROFILE,
    CompatibilityProfile,
    get_profile,
)
from vaipex_cross_browser.sharding import select_shard


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--compatibility-profile",
        action="store",
        default=DEFAULT_PROFILE,
        help="Versioned browser-context profile to apply.",
    )
    parser.addoption(
        "--shard-index",
        action="store",
        default=1,
        type=int,
        help="One-based shard number to execute.",
    )
    parser.addoption(
        "--shard-total",
        action="store",
        default=1,
        type=int,
        help="Total number of deterministic shards.",
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    shard_index = config.getoption("shard_index")
    shard_total = config.getoption("shard_total")
    try:
        selected_ids = set(
            select_shard(
                (item.nodeid for item in items),
                shard_index=shard_index,
                shard_total=shard_total,
            )
        )
    except ValueError as error:
        raise pytest.UsageError(str(error)) from error

    if shard_total == 1:
        return
    selected = [item for item in items if item.nodeid in selected_ids]
    deselected = [item for item in items if item.nodeid not in selected_ids]
    config.hook.pytest_deselected(items=deselected)
    items[:] = selected


@pytest.fixture(scope="session")
def compatibility_profile(pytestconfig: pytest.Config) -> CompatibilityProfile:
    return get_profile(pytestconfig.getoption("compatibility_profile"))


@pytest.fixture(scope="session")
def browser_context_args(
    compatibility_profile: CompatibilityProfile,
) -> dict[str, object]:
    return compatibility_profile.context_options()


@pytest.fixture(scope="session")
def settings(app_server: str) -> AutomationSettings:
    return AutomationSettings.from_environment(default_base_url=app_server)


@pytest.fixture(scope="session")
def traveler(settings: AutomationSettings) -> Traveler:
    return settings.traveler


@pytest.fixture
def configured_page(page: Page, settings: AutomationSettings) -> Page:
    page.set_default_timeout(settings.timeout_ms)
    page.set_default_navigation_timeout(settings.timeout_ms)
    return page
