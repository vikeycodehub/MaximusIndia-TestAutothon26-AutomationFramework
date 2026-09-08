"""
Smoke test proving the whole pipeline works: config -> fixtures -> page object ->
assertions -> reporting. Replace the assertions/URLs tomorrow with the real AUT.
"""
import allure
import pytest

from framework.pages.playwright_dev_home_page import PlaywrightDevHomePage


@allure.feature("Web - Smoke")
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.web
def test_homepage_loads(page):
    home = PlaywrightDevHomePage(page).open()
    assert "Playwright" in home.title(), "Homepage title should mention Playwright"


@allure.feature("Web - Smoke")
@pytest.mark.smoke
@pytest.mark.web
def test_search_returns_results(page):
    home = PlaywrightDevHomePage(page).open()
    home.search("locators")
    result_text = home.first_result_text()
    assert result_text, "Search should return at least one visible result"
