"""
Playwright's *Android* support (distinct from mobile-web emulation).

This connects to a REAL or EMULATED Android device over adb and can:
- launch Chrome / a WebView and automate it with normal Playwright APIs
- install/launch apps, tap coordinates, take device screenshots, run shell commands

It is NOT a full native-app automation replacement for Appium (no accessibility-tree
based native widget locators). If tomorrow's challenge requires deep native Android
app automation, fall back to Appium - but for hybrid apps / mobile Chrome / WebViews,
this lets you stay 100% in Python + Playwright.

Prerequisites on the runner machine:
- Android SDK platform-tools (adb) installed and on PATH
- USB debugging enabled on the device, or an emulator already running
- `adb devices` shows the target device as "device" (not "unauthorized")
"""
from __future__ import annotations

from playwright.sync_api import Playwright

from framework.core.logger import get_logger

logger = get_logger(__name__)


def get_first_android_device(playwright: Playwright):
    devices = playwright.android.devices()
    if not devices:
        raise RuntimeError(
            "No Android devices found via adb. Run `adb devices` to verify a device/emulator "
            "is connected and authorized before running Android tests."
        )
    logger.info("Found %d Android device(s), using the first one.", len(devices))
    return devices[0]


def launch_chrome_context(playwright: Playwright):
    """Launch Chrome on the connected Android device and return (device, context)."""
    device = get_first_android_device(playwright)
    context = device.launch_browser()
    return device, context
