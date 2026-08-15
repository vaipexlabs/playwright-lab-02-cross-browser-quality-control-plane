from __future__ import annotations

import pytest
from playwright.sync_api import Page

from tests.config import AutomationSettings, Traveler
from vaipex_cross_browser.profiles import (
    DEFAULT_PROFILE,
    CompatibilityProfile,
    get_profile,
)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--compatibility-profile",
        action="store",
        default=DEFAULT_PROFILE,
        help="Versioned browser-context profile to apply.",
    )


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
