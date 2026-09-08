"""
BasePage - shared Playwright actions every Page Object should inherit.

Keeping raw Playwright calls out of test files/page objects means:
- one place to add logging, waits, retries, screenshots
- tests stay readable and business-focused
"""
from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import Page, expect

from framework.config.settings import settings
from framework.core.logger import get_logger

logger = get_logger(__name__)

SCREENSHOT_DIR = Path(__file__).resolve().parents[2] / "reports" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = settings.default_timeout_ms

    # ---------- navigation ----------
    def goto(self, path: str = "") -> None:
        url = path if path.startswith("http") else f"{settings.base_url}{path}"
        logger.info("Navigating to %s", url)
        self.page.goto(url, timeout=self.timeout)

    # ---------- actions ----------
    def click(self, selector: str) -> None:
        logger.info("Click: %s", selector)
        self.page.locator(selector).click(timeout=self.timeout)

    def fill(self, selector: str, value: str) -> None:
        logger.info("Fill: %s -> %s", selector, "*" * len(value) if "pass" in selector.lower() else value)
        self.page.locator(selector).fill(value, timeout=self.timeout)

    def press(self, selector: str, key: str) -> None:
        self.page.locator(selector).press(key, timeout=self.timeout)

    # ---------- reads / assertions ----------
    def text_of(self, selector: str) -> str:
        return self.page.locator(selector).inner_text(timeout=self.timeout)

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible(timeout=self.timeout)

    def expect_text(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector)).to_contain_text(text, timeout=self.timeout)

    # ---------- waits ----------
    def wait_for_selector(self, selector: str, state: str = "visible") -> None:
        self.page.wait_for_selector(selector, state=state, timeout=self.timeout)

    # ---------- diagnostics ----------
    def screenshot(self, name: str) -> Path:
        filename = SCREENSHOT_DIR / f"{name}_{int(time.time())}.png"
        self.page.screenshot(path=str(filename), full_page=True)
        logger.info("Screenshot saved: %s", filename)
        return filename
