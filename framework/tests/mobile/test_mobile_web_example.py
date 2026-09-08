"""
Mobile-web emulation example using Playwright's built-in device descriptors
(Pixel/iPhone viewport, user-agent, touch). Runs on any machine, no adb needed.
Good for responsive-web validation of the AUT's mobile experience.
"""
import allure
import pytest

from framework.config.settings import settings


@allure.feature("Mobile Web - Smoke")
@pytest.mark.smoke
@pytest.mark.mobile_web
def test_mobile_homepage_renders(browser, playwright):
    # Use the shared `browser` fixture but build a mobile-emulated context explicitly
    # so this test is independent of the desktop browser_context_args override.
    pixel = playwright.devices["Pixel 7"]
    context = browser.new_context(**pixel, base_url=settings.base_url)
    page = context.new_page()
    page.goto("/")
    assert "Playwright" in page.title()
    page.close()
    context.close()
