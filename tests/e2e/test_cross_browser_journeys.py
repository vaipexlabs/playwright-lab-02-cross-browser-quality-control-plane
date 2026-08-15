import pytest
from playwright.sync_api import Page

from tests.config import AutomationSettings, Traveler
from tests.pages.explorer_page import ExplorerPage

pytestmark = [pytest.mark.e2e, pytest.mark.compatibility]


def test_customer_can_filter_and_build_a_plan(
    configured_page: Page,
    settings: AutomationSettings,
) -> None:
    explorer = ExplorerPage(configured_page, settings.base_url)
    explorer.open()
    explorer.filter_experiences("reliability")
    explorer.expect_only_experience("Kyoto Reliability Retreat")
    explorer.add_experience("Kyoto Reliability Retreat")
    explorer.expect_plan(["Kyoto Reliability Retreat"], "$1,120")


def test_customer_can_confirm_a_multi_city_plan(
    configured_page: Page,
    settings: AutomationSettings,
    traveler: Traveler,
) -> None:
    explorer = ExplorerPage(configured_page, settings.base_url)
    explorer.open()
    explorer.add_experience("Copenhagen Design Sprint")
    explorer.add_experience("Lisbon Platform Summit")
    explorer.expect_plan(
        ["Copenhagen Design Sprint", "Lisbon Platform Summit"],
        "$1,530",
    )
    explorer.confirm_plan(traveler)
