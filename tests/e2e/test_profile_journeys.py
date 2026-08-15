import pytest
from playwright.sync_api import Page, expect

from tests.config import AutomationSettings
from tests.pages.explorer_page import ExplorerPage
from vaipex_cross_browser.profiles import CompatibilityProfile

pytestmark = [pytest.mark.e2e, pytest.mark.compatibility]


def test_browser_context_matches_declared_profile(
    configured_page: Page,
    settings: AutomationSettings,
    compatibility_profile: CompatibilityProfile,
) -> None:
    explorer = ExplorerPage(configured_page, settings.base_url)
    explorer.open()

    assert configured_page.viewport_size == {
        "width": compatibility_profile.width,
        "height": compatibility_profile.height,
    }
    assert (
        configured_page.evaluate("navigator.language") == compatibility_profile.locale
    )
    assert (
        configured_page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone")
        == compatibility_profile.timezone_id
    )
    assert bool(configured_page.evaluate("navigator.maxTouchPoints > 0")) is (
        compatibility_profile.touch
    )
    assert bool(
        configured_page.evaluate(
            "matchMedia('(prefers-reduced-motion: reduce)').matches"
        )
    ) is (compatibility_profile.reduced_motion == "reduce")

    menu = configured_page.get_by_test_id("mobile-menu-toggle")
    navigation = configured_page.get_by_role("navigation", name="Primary")
    if compatibility_profile.width <= 680:
        expect(menu).to_be_visible()
        expect(navigation).to_be_hidden()
        menu.click()
        expect(navigation).to_be_visible()
    else:
        expect(menu).to_be_hidden()
        expect(navigation).to_be_visible()


def test_customer_outcome_survives_declared_profile(
    configured_page: Page,
    settings: AutomationSettings,
) -> None:
    explorer = ExplorerPage(configured_page, settings.base_url)
    explorer.open()
    expected_price = explorer.displayed_price("Kyoto Reliability Retreat")
    explorer.filter_experiences("reliability")
    explorer.expect_only_experience("Kyoto Reliability Retreat")
    explorer.add_experience("Kyoto Reliability Retreat")
    explorer.expect_plan(["Kyoto Reliability Retreat"], expected_price)
