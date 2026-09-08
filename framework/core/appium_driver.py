"""
Appium driver factory for NATIVE Android app automation.

This is the fallback/complementary track to Playwright when tomorrow's challenge
turns out to be a native Android app (not web/hybrid). Requires:
- Appium server running (see scripts/start_appium_server.ps1)
- Android SDK + emulator running, or a real device connected via adb (USB debugging on)
- `ANDROID_APP_PATH` set in .env once the real APK is provided (optional if the app
  is already installed on the device - then just set ANDROID_APP_PACKAGE/ACTIVITY)
"""
from __future__ import annotations

from appium import webdriver
from appium.options.android import UiAutomator2Options

from framework.config.settings import settings
from framework.core.logger import get_logger

logger = get_logger(__name__)


def build_android_driver() -> webdriver.Remote:
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = settings.android_device_name
    options.app_package = settings.android_app_package
    options.app_activity = settings.android_app_activity
    options.no_reset = True
    options.new_command_timeout = 120

    if settings.android_platform_version:
        options.platform_version = settings.android_platform_version

    if settings.android_app_path:
        # Installs/launches the given APK instead of relying on an already-installed app.
        options.app = settings.android_app_path

    logger.info(
        "Starting Appium session: server=%s package=%s activity=%s",
        settings.appium_server_url,
        settings.android_app_package,
        settings.android_app_activity,
    )
    driver = webdriver.Remote(settings.appium_server_url, options=options)
    driver.implicitly_wait(10)
    return driver


def appium_server_reachable() -> bool:
    """Quick check so tests can skip cleanly instead of erroring when Appium isn't running."""
    import urllib.request

    try:
        status_url = settings.appium_server_url.rstrip("/") + "/status"
        with urllib.request.urlopen(status_url, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False
