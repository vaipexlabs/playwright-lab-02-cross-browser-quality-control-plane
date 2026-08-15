from __future__ import annotations

import re

from playwright.sync_api import Page, expect

from tests.config import Traveler


class ExplorerPage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.search = page.get_by_test_id("experience-search")
        self.cards = page.get_by_test_id("experience-card")
        self.plan = page.get_by_test_id("plan-summary")

    def open(self) -> None:
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Vaipex Explorer")
        expect(
            self.page.get_by_role(
                "heading",
                name="Plan work that broadens your perspective.",
            )
        ).to_be_visible()

    def filter_experiences(self, query: str) -> None:
        self.search.fill(query)

    def expect_only_experience(self, name: str) -> None:
        expect(self.cards.filter(visible=True)).to_have_count(1)
        expect(self.cards.filter(visible=True)).to_contain_text(name)

    def add_experience(self, name: str) -> None:
        card = self.cards.filter(has_text=name)
        expect(card).to_have_count(1)
        card.get_by_role("button", name="Add to plan").click()
        expect(card.get_by_role("button", name="Added")).to_be_disabled()

    def expect_plan(self, names: list[str], total: str) -> None:
        for name in names:
            expect(self.plan).to_contain_text(name)
        expect(self.plan.locator("[data-plan-total]")).to_have_text(total)

    def confirm_plan(self, traveler: Traveler) -> None:
        self.plan.get_by_role("button", name="Review and confirm").click()
        dialog = self.page.get_by_role("dialog", name="Confirm your plan")
        expect(dialog).to_be_visible()
        dialog.get_by_label("Traveler name").fill(traveler.name)
        dialog.get_by_label("Traveler email").fill(traveler.email)
        dialog.get_by_role("button", name="Confirm booking").click()
        expect(dialog.get_by_role("heading", name="Plan confirmed")).to_be_visible()
        expect(dialog.locator("[data-booking-id]")).to_have_text(
            re.compile(r"^VXP-[A-F0-9]{6}$")
        )
