"""
BaseMobilePage - shared Appium actions for native Android Page Objects.

Mirrors framework/core/base_page.py (the Playwright web equivalent) so the
team can switch mental models quickly: same method names, different driver.
"""
from __future__ import annotations

import time
from pathlib import Path

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from framework.core.logger import get_logger

logger = get_logger(__name__)

SCREENSHOT_DIR = Path(__file__).resolve().parents[2] / "reports" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


class BaseMobilePage:
    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.timeout = timeout

    # ---------- locators: use resource-id by default, accept any AppiumBy strategy ----------
    def _find(self, by: str, value: str):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def find_by_id(self, resource_id: str):
        return self._find(AppiumBy.ID, resource_id)

    def find_by_xpath(self, xpath: str):
        return self._find(AppiumBy.XPATH, xpath)

    def find_by_accessibility_id(self, name: str):
        return self._find(AppiumBy.ACCESSIBILITY_ID, name)

    # ---------- actions ----------
    def tap(self, by: str, value: str) -> None:
        logger.info("Tap: %s=%s", by, value)
        self._find(by, value).click()

    def type_text(self, by: str, value: str, text: str) -> None:
        logger.info("Type into %s=%s", by, value)
        el = self._find(by, value)
        el.clear()
        el.send_keys(text)

    def text_of(self, by: str, value: str) -> str:
        return self._find(by, value).text

    def is_present(self, by: str, value: str) -> bool:
        try:
            self._find(by, value)
            return True
        except Exception:
            return False

    # ---------- gestures ----------
    def swipe_up(self) -> None:
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.8)
        end_y = int(size["height"] * 0.2)
        self.driver.swipe(start_x, start_y, start_x, end_y, 400)

    def press_back(self) -> None:
        self.driver.back()

    # ---------- diagnostics ----------
    def screenshot(self, name: str) -> Path:
        filename = SCREENSHOT_DIR / f"{name}_{int(time.time())}.png"
        self.driver.get_screenshot_as_file(str(filename))
        logger.info("Screenshot saved: %s", filename)
        return filename
