"""
Sample Page Object for https://playwright.dev - proves the framework wiring end to end.

Tomorrow: delete/replace this with real page objects for the actual AUT, following
the same pattern (inherit BasePage, define selectors as constants, expose intent-based
methods like `search_docs()` rather than leaking raw selectors into tests).
"""
from __future__ import annotations

from framework.core.base_page import BasePage


class PlaywrightDevHomePage(BasePage):
    SEARCH_BUTTON = "button.DocSearch-Button"
    SEARCH_INPUT = "input#docsearch-input"
    GET_STARTED_LINK = "a.getStarted_Sjon"

    def open(self) -> "PlaywrightDevHomePage":
        self.goto("/")
        return self

    def title(self) -> str:
        return self.page.title()

    def open_search(self) -> "PlaywrightDevHomePage":
        self.click(self.SEARCH_BUTTON)
        return self

    def search(self, term: str) -> "PlaywrightDevHomePage":
        self.open_search()
        self.page.locator(self.SEARCH_INPUT).fill(term)
        return self

    def first_result_text(self) -> str:
        result = self.page.locator(".DocSearch-Hit").first
        result.wait_for(state="visible", timeout=self.timeout)
        return result.inner_text()
