"""
Real/emulated Android device automation via Playwright's adb-based Android support.

Skips gracefully if no device is connected - safe to keep in the suite. Use this
track only if tomorrow's Android challenge is a WebView/hybrid app or mobile Chrome.
For pure native-app UI automation, use Appium instead (not covered by Playwright).
"""
import pytest
from playwright.sync_api import sync_playwright

from framework.core.android_driver import launch_chrome_context


def _android_device_available() -> bool:
    try:
        with sync_playwright() as p:
            return len(p.android.devices()) > 0
    except Exception:
        return False


@pytest.mark.android
@pytest.mark.skipif(not _android_device_available(), reason="No Android device/emulator connected via adb")
def test_android_chrome_loads_homepage():
    with sync_playwright() as p:
        device, context = launch_chrome_context(p)
        try:
            page = context.new_page()
            page.goto("https://playwright.dev")
            assert "Playwright" in page.title()
        finally:
            context.close()
            device.close()
